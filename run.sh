#!/bin/bash
# Helper script to run the Blink archiver
# Can be used with cron or systemd

cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the archiver
python3 blink_archiver.py "$@"
