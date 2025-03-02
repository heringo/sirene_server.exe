#!/bin/bash
set -e

# Update and upgrade the system packages
echo "Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install essential system packages
echo "Installing Python3, pip, git, cron and other essentials..."
sudo apt-get install -y python3 python3-pip git cron wget curl unzip

# Install Google Chrome if not already installed
if ! command -v google-chrome &>/dev/null; then
    echo "Installing Google Chrome..."
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i google-chrome-stable_current_amd64.deb || sudo apt-get install -fy
    rm google-chrome-stable_current_amd64.deb
else
    echo "Google Chrome is already installed."
fi

# (Optional) Clone your project repository if needed.
# Uncomment and adjust the following lines if your project is hosted on git.
# echo "Cloning your project repository..."
# git clone https://your-repo-url.git /opt/myproject
# cd /opt/myproject

# If your project code is already on the VPS, make sure you're in the project folder:
# cd /path/to/your/project

# Upgrade pip and install Python dependencies from requirements.txt
echo "Installing Python dependencies..."
pip3 install --upgrade pip
if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt
else
    echo "requirements.txt not found. Please ensure it is in your project directory."
    exit 1
fi

# Create or update a cron job to run main.py every Monday at 1am
# Define the full paths to your Python interpreter and main.py.
PYTHON_PATH="$(which python3)"
MAIN_PY="/full/path/to/main.py"  # Update this with the absolute path to your main.py file
LOG_FILE="/full/path/to/main.log"  # Update this log file path if desired

echo "Setting up cron job to run main.py every Monday at 1am..."
CRON_JOB="0 1 * * 1 $PYTHON_PATH $MAIN_PY >> $LOG_FILE 2>&1"

# Check if the cron job already exists and add it if not.
(crontab -l 2>/dev/null | grep -F "$CRON_JOB") || (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

# Ensure the cron service is enabled and started.
echo "Ensuring cron service is running..."
sudo systemctl enable cron
sudo systemctl start cron

echo "Setup complete. Your project is installed and the cron job has been scheduled."
