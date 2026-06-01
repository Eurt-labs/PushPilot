#!/usr/bin/env bash

# Exit on error
set -e

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== PushPilot Linux Builder ===${NC}"

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed or not in PATH.${NC}"
    echo -e "Please install Python 3 using your system package manager."
    exit 1
fi

# Check for pip
if ! python3 -m pip --version &> /dev/null; then
    echo -e "${YELLOW}Warning: pip is not installed or not working.${NC}"
    echo -e "Attempting to install pip..."
    sudo apt install python3-pip || sudo dnf install python3-pip || sudo pacman -S python-pip || {
        echo -e "${RED}Could not automatically install pip. Please install pip first.${NC}"
        exit 1
    }
fi

# Check for Tkinter
echo -e "${GREEN}Checking Tkinter installation...${NC}"
if ! python3 -c "import tkinter" &> /dev/null; then
    echo -e "${YELLOW}Warning: Tkinter (required for GUI) was not found.${NC}"
    echo -e "You might need to install it manually using your package manager:"
    echo -e "  - Ubuntu/Debian: ${GREEN}sudo apt install python3-tk${NC}"
    echo -e "  - Fedora:        ${GREEN}sudo dnf install python3-tkinter${NC}"
    echo -e "  - Arch Linux:    ${GREEN}sudo pacman -S tk${NC}"
    echo -e "Press Enter to continue anyway, or Ctrl+C to abort and install it first..."
    read -r
fi

# Install pyinstaller if not present
if ! command -v pyinstaller &> /dev/null; then
    echo -e "${YELLOW}PyInstaller not found. Installing PyInstaller...${NC}"
    python3 -m pip install --upgrade pip
    python3 -m pip install pyinstaller
fi

# Delete existing Linux binary if it exists to avoid conflicts
if [ -f "Desktop application/PushPilot" ]; then
    echo -e "${YELLOW}Removing existing PushPilot binary...${NC}"
    rm "Desktop application/PushPilot"
fi

echo -e "${GREEN}Building standalone Linux application using PyInstaller...${NC}"
pyinstaller --onefile autocommit_app.py \
            --name PushPilot \
            --distpath "Desktop application" \
            --workpath build \
            --specpath build

if [ -f "Desktop application/PushPilot" ]; then
    # Make sure it's executable
    chmod +x "Desktop application/PushPilot"
    echo -e "${GREEN}=== Build Successful! ===${NC}"
    echo -e "The Linux binary is located at: ${YELLOW}Desktop application/PushPilot${NC}"
    echo -e "To run the GUI: ${GREEN}./Desktop\ application/PushPilot${NC}"
    echo -e "To run the CLI: ${GREEN}./Desktop\ application/PushPilot setup --remote <URL>${NC}"
else
    echo -e "${RED}Error: Build failed. Standalone binary was not created.${NC}"
    exit 1
fi
