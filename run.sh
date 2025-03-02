#!/bin/bash
# This script installs a cron job to run main.py every Monday at 1am.

# Absolute path to your Python interpreter (adjust as needed)
PYTHON="/usr/bin/python3"

# Absolute path to your main.py (update to the correct location)
MAIN_PY="/main.py"

# Optional: log file for output (update path if desired)
LOG_FILE="/main.log"

# The cron job entry: run main.py every Monday at 1am
CRON_JOB="0 1 * * 1 $PYTHON $MAIN_PY >> $LOG_FILE 2>&1"

# Check if the cron job is already installed.
(crontab -l 2>/dev/null | grep -F "$CRON_JOB") && {
    echo "Cron job already installed."
    exit 0
}

# Install the new cron job.
( crontab -l 2>/dev/null; echo "$CRON_JOB" ) | crontab -

echo "Cron job installed: main.py will run every Monday at 1am."
