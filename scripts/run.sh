#!/bin/bash
# This script installs a cron job to run main.py every Monday at 1am.

# Get the absolute path of the current project directory.
PROJECT_DIR="$(pwd)"

# Absolute path to the Python interpreter inside the virtual environment.
PYTHON="$PROJECT_DIR/venv/bin/python"

# Absolute path to your main.py script (adjust if your file is located elsewhere).
MAIN_PY="$PROJECT_DIR/src/main.py"

# Optional: absolute path to the log file for output.
LOG_FILE="$PROJECT_DIR/src/main.log"

# The cron job entry: run main.py every Monday at 1am.
CRON_JOB="0 1 * * 1 $PYTHON $MAIN_PY >> $LOG_FILE 2>&1"

# Check if the cron job is already installed.
if crontab -l 2>/dev/null | grep -F "$CRON_JOB" > /dev/null; then
    echo "Cron job already installed."
    exit 0
fi

# Install the new cron job.
( crontab -l 2>/dev/null; echo "$CRON_JOB" ) | crontab -

echo "Cron job installed: main.py will run every Monday at 1am."
