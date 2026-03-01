#!/bin/bash
set -e

# Devil's Advocate Uninstallation Script for OpenCode

CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"

echo "Removing Devil's Advocate Skill & Command from OpenCode..."

# Remove command file
if [ -f "$CONFIG_DIR/commands/devils-advocate.md" ]; then
    rm "$CONFIG_DIR/commands/devils-advocate.md"
    echo "✅ Command /devils-advocate removed successfully."
else
    echo "⚠️ Command /devils-advocate not found."
fi

# Remove skill directory
if [ -d "$CONFIG_DIR/skills/devils-advocate" ]; then
    rm -rf "$CONFIG_DIR/skills/devils-advocate"
    echo "✅ Skill devils-advocate removed successfully."
else
    echo "⚠️ Skill devils-advocate not found."
fi

echo ""
echo "Uninstallation complete!"
