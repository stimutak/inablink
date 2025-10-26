#!/usr/bin/env python3
"""
Blink Camera Archiver

Automatically downloads and archives video clips from Blink home security cameras
at regular intervals to protect against tampering or cloud deletion.
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Set, Optional
import argparse

from aiohttp import ClientSession
from blinkpy.blinkpy import Blink
from blinkpy.auth import Auth
from blinkpy.helpers.util import json_load


class BlinkArchiver:
    """Manages authentication and archival of Blink camera videos."""

    def __init__(self, config_path: str = "config.json"):
        """Initialize the archiver with configuration."""
        self.config = self._load_config(config_path)
        self._setup_logging()

        self.blink: Optional[Blink] = None
        self.download_path = Path(self.config["download_path"])
        self.archive_db_path = Path(self.config["archive_db_path"])
        self.archive_db: Dict[str, Set[str]] = self._load_archive_db()

        # Create download directory
        self.download_path.mkdir(parents=True, exist_ok=True)

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file '{config_path}' not found.")
            print("Please copy 'config.example.json' to 'config.json' and update with your credentials.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in configuration file: {e}")
            sys.exit(1)

    def _setup_logging(self):
        """Configure logging based on config settings."""
        log_level = getattr(logging, self.config.get("log_level", "INFO"))
        log_file = self.config.get("log_file", "blink_archiver.log")

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _load_archive_db(self) -> Dict[str, Set[str]]:
        """Load the database of previously downloaded videos."""
        if self.archive_db_path.exists():
            try:
                with open(self.archive_db_path, 'r') as f:
                    data = json.load(f)
                    # Convert lists back to sets
                    return {k: set(v) for k, v in data.items()}
            except (json.JSONDecodeError, IOError) as e:
                self.logger.warning(f"Could not load archive database: {e}. Starting fresh.")
                return {}
        return {}

    def _save_archive_db(self):
        """Save the database of downloaded videos."""
        try:
            # Convert sets to lists for JSON serialization
            data = {k: list(v) for k, v in self.archive_db.items()}
            with open(self.archive_db_path, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            self.logger.error(f"Failed to save archive database: {e}")

    async def authenticate(self) -> bool:
        """Authenticate with Blink servers."""
        try:
            self.logger.info("Authenticating with Blink...")

            # Create auth object
            auth = Auth(
                {
                    "username": self.config["username"],
                    "password": self.config["password"]
                },
                no_prompt=False  # Allow 2FA prompt if needed
            )

            # Create Blink instance
            self.blink = Blink(session=ClientSession())
            self.blink.auth = auth

            # Attempt to start session
            await self.blink.start()

            # Check if we need 2FA
            if self.blink.auth.check_key_required():
                self.logger.info("2FA required. Please check your email/phone for the code.")
                await self.blink.setup_post_verify()

            self.logger.info("Authentication successful!")
            return True

        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            return False

    async def get_all_cameras(self) -> Dict[str, any]:
        """Retrieve all cameras from the Blink system."""
        if not self.blink:
            self.logger.error("Not authenticated. Call authenticate() first.")
            return {}

        try:
            # Refresh to get latest camera data
            await self.blink.refresh(force=False)
            return self.blink.cameras
        except Exception as e:
            self.logger.error(f"Failed to retrieve cameras: {e}")
            return {}

    async def download_new_videos(self, since_date: Optional[datetime] = None) -> int:
        """
        Download videos that haven't been archived yet.

        Args:
            since_date: Only download videos from this date onwards.
                       If None, downloads from last 24 hours.

        Returns:
            Number of videos downloaded
        """
        if not self.blink:
            self.logger.error("Not authenticated. Call authenticate() first.")
            return 0

        if since_date is None:
            since_date = datetime.now() - timedelta(days=1)

        try:
            # Refresh camera list
            await self.blink.refresh()

            cameras = self.blink.cameras
            if not cameras:
                self.logger.warning("No cameras found in your Blink system.")
                return 0

            self.logger.info(f"Found {len(cameras)} camera(s)")

            total_downloaded = 0

            for camera_name, camera in cameras.items():
                self.logger.info(f"Processing camera: {camera_name}")

                # Create camera-specific directory
                camera_path = self.download_path / self._sanitize_filename(camera_name)
                camera_path.mkdir(parents=True, exist_ok=True)

                # Initialize archive tracking for this camera
                if camera_name not in self.archive_db:
                    self.archive_db[camera_name] = set()

                # Get videos for this camera
                try:
                    # Request video list
                    await camera.get_media()

                    if not camera.recent_clips:
                        self.logger.info(f"No recent clips for {camera_name}")
                        continue

                    # Process each clip
                    for clip in camera.recent_clips:
                        clip_id = str(clip.get('id', ''))
                        created_at = clip.get('created_at', '')

                        # Skip if already downloaded
                        if clip_id in self.archive_db[camera_name]:
                            self.logger.debug(f"Skipping already archived clip: {clip_id}")
                            continue

                        # Parse date if available
                        try:
                            clip_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                            if clip_date < since_date:
                                self.logger.debug(f"Skipping clip older than {since_date}: {clip_id}")
                                continue
                        except (ValueError, AttributeError):
                            self.logger.warning(f"Could not parse date for clip {clip_id}, downloading anyway")

                        # Download the clip
                        try:
                            address = clip.get('media', '')
                            if not address:
                                self.logger.warning(f"No media URL for clip {clip_id}")
                                continue

                            # Generate filename with date
                            date_str = created_at.replace(':', '-').replace('T', '_').split('.')[0] if created_at else 'unknown'
                            filename = f"{date_str}_{clip_id}.mp4"
                            filepath = camera_path / filename

                            # Download video
                            response = await camera.get_video_response(address)

                            if response.status == 200:
                                video_data = await response.read()

                                # Save to file
                                with open(filepath, 'wb') as f:
                                    f.write(video_data)

                                self.logger.info(f"Downloaded: {filename} ({len(video_data)} bytes)")

                                # Mark as archived
                                self.archive_db[camera_name].add(clip_id)
                                total_downloaded += 1

                                # Save database after each successful download
                                self._save_archive_db()
                            else:
                                self.logger.error(f"Failed to download {clip_id}: HTTP {response.status}")

                        except Exception as e:
                            self.logger.error(f"Error downloading clip {clip_id}: {e}")
                            continue

                except Exception as e:
                    self.logger.error(f"Error processing camera {camera_name}: {e}")
                    continue

            self.logger.info(f"Downloaded {total_downloaded} new video(s)")
            return total_downloaded

        except Exception as e:
            self.logger.error(f"Error in download_new_videos: {e}")
            return 0

    def _sanitize_filename(self, filename: str) -> str:
        """Remove invalid characters from filename."""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

    async def run_once(self):
        """Run a single check and download cycle."""
        self.logger.info("Starting single archive run...")

        if not await self.authenticate():
            self.logger.error("Authentication failed. Exiting.")
            return

        try:
            await self.download_new_videos()
        finally:
            await self.cleanup()

    async def run_continuous(self):
        """Run continuous monitoring at configured intervals."""
        interval = self.config.get("check_interval_seconds", 300)

        # Ensure we respect Blink's 60-second minimum
        if interval < 60:
            self.logger.warning(f"Check interval {interval}s is too short. Using 60s minimum.")
            interval = 60

        self.logger.info(f"Starting continuous monitoring (checking every {interval} seconds)...")

        if not await self.authenticate():
            self.logger.error("Authentication failed. Exiting.")
            return

        try:
            while True:
                try:
                    await self.download_new_videos()
                except Exception as e:
                    self.logger.error(f"Error during download cycle: {e}")

                self.logger.info(f"Sleeping for {interval} seconds...")
                await asyncio.sleep(interval)

        except KeyboardInterrupt:
            self.logger.info("Received shutdown signal.")
        finally:
            await self.cleanup()

    async def cleanup(self):
        """Clean up resources."""
        if self.blink and self.blink.auth.session:
            await self.blink.auth.session.close()
        self.logger.info("Cleanup complete.")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Blink Camera Archiver - Archive your Blink security camera videos"
    )
    parser.add_argument(
        '--config',
        default='config.json',
        help='Path to configuration file (default: config.json)'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once and exit (default: run continuously)'
    )
    parser.add_argument(
        '--since-days',
        type=int,
        default=1,
        help='Download videos from the last N days (default: 1)'
    )

    args = parser.parse_args()

    archiver = BlinkArchiver(config_path=args.config)

    if args.once:
        await archiver.run_once()
    else:
        await archiver.run_continuous()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown requested. Exiting...")
        sys.exit(0)
