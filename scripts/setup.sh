#!/bin/bash
set -e

# Update and upgrade the system packages
echo "Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install essential system packages (including python3-venv)
echo "Installing Python3, pip, git, cron and other essentials..."
sudo apt-get install -y python3 python3-pip python3-venv git cron wget curl unzip

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

# Ensure you are in your project directory.
# cd /path/to/your/project

# Create a virtual environment if it does not exist
VENV_DIR="./venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip inside the virtual environment
echo "Upgrading pip in the virtual environment..."
pip install --upgrade pip

# Install Python dependencies from requirements.txt in the project root
echo "Installing Python dependencies from requirements.txt..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found in the current directory. Please ensure it is in your project directory."
    exit 1
fi