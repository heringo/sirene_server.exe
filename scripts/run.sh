# Define the full paths to your Python interpreter (from the virtual environment) and main.py.
PYTHON_PATH="$(pwd)/venv/bin/python"
MAIN_PY="$(pwd)/src/main.py"   # Update if your main.py is in a different location
LOG_FILE="$(pwd)/src/main.log"  # Update log file path if desired

# Create or update a cron job to run main.py every Monday at 1am
echo "Setting up cron job to run main.py every Monday at 1am..."
CRON_JOB="0 1 * * 1 $PYTHON_PATH $MAIN_PY >> $LOG_FILE 2>&1"

# Check if the cron job already exists; if not, add it.
(crontab -l 2>/dev/null | grep -F "$CRON_JOB") || (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

# Ensure the cron service is enabled and started.
echo "Ensuring cron service is running..."
sudo systemctl enable cron
sudo systemctl start cron

echo "Setup complete. Your project is installed and the cron job has been scheduled."
