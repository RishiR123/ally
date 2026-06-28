#!/usr/bin/env bash

# Ally CLI Agent Uninstallation Script
# This script removes the global installation of Ally from ~/.ally and ~/.local/bin/ally

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Uninstalling Ally CLI Agent...${NC}"

ALLY_DIR="$HOME/.ally"
WRAPPER_SCRIPT="$HOME/.local/bin/ally"

# Remove the executable wrapper
if [ -f "$WRAPPER_SCRIPT" ]; then
    echo -e "Removing executable wrapper from $WRAPPER_SCRIPT..."
    rm "$WRAPPER_SCRIPT"
else
    echo -e "Executable wrapper not found at $WRAPPER_SCRIPT."
fi

# Remove the installation directory
if [ -d "$ALLY_DIR" ]; then
    echo -e "Removing installation directory $ALLY_DIR..."
    rm -rf "$ALLY_DIR"
else
    echo -e "Installation directory not found at $ALLY_DIR."
fi

echo -e "\n${GREEN}Uninstallation complete!${NC}"
echo -e "Ally has been completely removed from your system."
