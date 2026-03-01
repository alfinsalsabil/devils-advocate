#!/bin/bash
set -e

# Devil's Advocate Installation Script for OpenCode

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"

echo "Installing Devil's Advocate Skill & Command for OpenCode..."

# Check if source files exist
if [ ! -f "$SCRIPT_DIR/commands/devils-advocate.md" ] || [ ! -f "$SCRIPT_DIR/skills/devils-advocate/SKILL.md" ]; then
    echo "❌ Error: Source files not found. Make sure you are running this from a complete repository."
    exit 1
fi

# Create directories if they don't exist
mkdir -p "$CONFIG_DIR/commands"
mkdir -p "$CONFIG_DIR/skills/devils-advocate"

# Copy command file
cp "$SCRIPT_DIR/commands/devils-advocate.md" "$CONFIG_DIR/commands/"
echo "✅ Command /devils-advocate installed successfully."

# Copy skill file
cp "$SCRIPT_DIR/skills/devils-advocate/SKILL.md" "$CONFIG_DIR/skills/devils-advocate/"
echo "✅ Skill devils-advocate installed successfully."

echo ""
echo "Installation complete! You can now use the '/devils-advocate <prompt>' command in OpenCode."
