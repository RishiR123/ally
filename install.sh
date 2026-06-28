#!/usr/bin/env bash

# Ally CLI Agent Installation Script
# This script installs Ally to ~/.ally and creates a wrapper in ~/.local/bin

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Installing Ally CLI Agent...${NC}"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

ALLY_DIR="$HOME/.ally"
VENV_DIR="$ALLY_DIR/venv"
SRC_DIR="$ALLY_DIR/src"
BIN_DIR="$HOME/.local/bin"

# Create directories
mkdir -p "$ALLY_DIR"
mkdir -p "$BIN_DIR"

# Handle source code
echo -e "Setting up source code..."
if [ -d "$SRC_DIR" ]; then
    echo -e "Updating existing source..."
    cd "$SRC_DIR"
    git pull || true
else
    # In a real scenario, this would clone from the public repo:
    # git clone https://github.com/RishiR123/ally.git "$SRC_DIR"
    
    # For now, since we might be running this locally from the dev repo:
    if [ -f "pyproject.toml" ]; then
       echo -e "Copying local source to $SRC_DIR..."
       cp -R . "$SRC_DIR"
    else
       echo -e "Cloning repository..."
       git clone https://github.com/RishiR123/ally.git "$SRC_DIR"
    fi
fi

# Set up virtual environment
echo -e "Creating virtual environment in $VENV_DIR..."
python3 -m venv "$VENV_DIR"

# Install dependencies
echo -e "Installing dependencies..."
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -e "$SRC_DIR"

# Create executable wrapper
WRAPPER_SCRIPT="$BIN_DIR/ally"
echo -e "Creating executable wrapper at $WRAPPER_SCRIPT..."

cat > "$WRAPPER_SCRIPT" << EOF
#!/usr/bin/env bash
# Wrapper to run Ally with its virtual environment
source "$VENV_DIR/bin/activate"
python -m ally.cli "\$@"
EOF

chmod +x "$WRAPPER_SCRIPT"

echo -e "\n${GREEN}Installation complete!${NC}"
echo -e "Ally has been installed to $ALLY_DIR."
echo -e "The executable is located at $BIN_DIR/ally."
echo -e "\n${BLUE}IMPORTANT:${NC}"
echo -e "Please make sure ${GREEN}$BIN_DIR${NC} is in your PATH."
echo -e "You can add it by running this command:"
echo -e "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc && source ~/.zshrc"
echo -e "\nOnce your PATH is set, simply type ${GREEN}ally${NC} to start the interactive setup!"
