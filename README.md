# Blink Camera Archiver

Automatically download and archive video clips from your Blink home security cameras to protect against tampering or cloud deletion. This tool runs at regular intervals and saves all new videos to your local storage.

## Features

- Automatic video archiving from all Blink cameras
- Tracks downloaded videos to avoid duplicates
- Organizes videos by camera name and date
- Respects Blink's API rate limits (60-second minimum)
- Supports 2FA authentication
- Configurable check intervals
- Can run as one-time check or continuous daemon
- Comprehensive logging
- Lightweight and efficient

## Requirements

- Python 3.8 or later
- Blink account with active cameras
- Internet connection

## Quick Start

### 1. Setup

Run the automated setup script:

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Create a config.json file from the example

### 2. Configure

Edit `config.json` with your Blink credentials:

```json
{
  "username": "your_blink_email@example.com",
  "password": "your_blink_password",
  "download_path": "./videos",
  "check_interval_seconds": 300,
  "archive_db_path": "./archive_db.json",
  "log_file": "./blink_archiver.log",
  "log_level": "INFO"
}
```

### 3. Run

Run once to test:
```bash
./run.sh --once
```

Run continuously:
```bash
./run.sh
```

Run in background:
```bash
nohup ./run.sh &
```

## Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and edit config
cp config.example.json config.json
# Edit config.json with your credentials

# Run
python3 blink_archiver.py
```

## Usage

```bash
python3 blink_archiver.py [OPTIONS]
```

### Options

- `--config PATH` - Path to configuration file (default: config.json)
- `--once` - Run once and exit (default: run continuously)
- `--since-days N` - Download videos from the last N days (default: 1)

### Examples

Run a single check:
```bash
python3 blink_archiver.py --once
```

Download videos from the last 7 days:
```bash
python3 blink_archiver.py --once --since-days 7
```

Run with custom config:
```bash
python3 blink_archiver.py --config /path/to/config.json
```

## Configuration

### Configuration Options

- `username` - Your Blink account email
- `password` - Your Blink account password
- `download_path` - Directory where videos will be saved
- `check_interval_seconds` - How often to check for new videos (minimum 60)
- `archive_db_path` - Path to the archive tracking database
- `log_file` - Path to the log file
- `log_level` - Logging level (DEBUG, INFO, WARNING, ERROR)

### Two-Factor Authentication

If your account has 2FA enabled, you'll be prompted to enter the code when running the archiver. The code will be sent to your registered email or phone.

## Directory Structure

After running, your directory will look like:

```
inablink/
├── blink_archiver.py       # Main script
├── config.json             # Your configuration (not in git)
├── archive_db.json         # Tracks downloaded videos (not in git)
├── blink_archiver.log      # Log file (not in git)
├── videos/                 # Downloaded videos directory
│   ├── Front_Door/         # Camera-specific folders
│   │   ├── 2025-01-15_12-30-00_12345.mp4
│   │   └── 2025-01-15_14-15-30_12346.mp4
│   └── Backyard/
│       └── 2025-01-15_13-00-00_12347.mp4
├── requirements.txt
├── setup.sh
├── run.sh
└── README.md
```

## Running as a Service

### Using systemd (Linux)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/blink-archiver.service
```

Add the following content (adjust paths):

```ini
[Unit]
Description=Blink Camera Archiver
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/inablink
ExecStart=/path/to/inablink/run.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable blink-archiver
sudo systemctl start blink-archiver
sudo systemctl status blink-archiver
```

View logs:
```bash
sudo journalctl -u blink-archiver -f
```

### Using cron (Linux/macOS)

For periodic checks, add to crontab:

```bash
crontab -e
```

Add a line (runs every 5 minutes):
```
*/5 * * * * /path/to/inablink/run.sh --once >> /path/to/inablink/cron.log 2>&1
```

### Using launchd (macOS)

Create a plist file at `~/Library/LaunchAgents/com.blink.archiver.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.blink.archiver</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/inablink/run.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/path/to/inablink</string>
    <key>StandardOutPath</key>
    <string>/path/to/inablink/stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/inablink/stderr.log</string>
</dict>
</plist>
```

Load the agent:
```bash
launchctl load ~/Library/LaunchAgents/com.blink.archiver.plist
```

## Troubleshooting

### Authentication Fails

- Verify your username and password in config.json
- If using 2FA, make sure you can receive the code
- Check if your account is locked or requires password reset

### No Videos Downloaded

- Ensure your cameras have recorded videos
- Check that videos exist in the Blink app
- Try reducing the `since-days` parameter
- Check logs for errors

### Rate Limit Errors

- Ensure `check_interval_seconds` is at least 60
- Reduce frequency of checks if you hit rate limits
- The Blink API recommends intervals of 60 seconds or more

### Videos Not Saving

- Check write permissions on the download directory
- Ensure sufficient disk space
- Check logs for I/O errors

## Security Notes

- Keep your `config.json` secure - it contains your credentials
- The `.gitignore` file prevents committing sensitive files
- Consider using environment variables for credentials in production
- Regularly backup your archived videos

## How It Works

1. Authenticates with Blink servers using your credentials
2. Retrieves list of all cameras on your account
3. For each camera, fetches recent video clips
4. Checks against local database to avoid re-downloading
5. Downloads new videos and saves them organized by camera
6. Updates tracking database
7. Waits for configured interval and repeats

## API Rate Limiting

This tool respects Blink's API guidelines:
- Minimum 60-second interval between checks
- Default check interval is 300 seconds (5 minutes)
- Forces delays between operations to prevent server overload

## Credits

Built using the [blinkpy](https://github.com/fronzbot/blinkpy) library for Blink API access.

## License

MIT License - See LICENSE file for details

## Contributing

Issues and pull requests welcome at the project repository.

## Disclaimer

This tool is not affiliated with or endorsed by Blink or Amazon. Use at your own risk. Ensure you comply with Blink's Terms of Service.