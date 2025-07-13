#!/bin/bash

# Script to set up VS Code workspace settings in devcontainer
# This ensures VS Code settings are available only in the container environment

set -e

# Detect workspace root - try multiple common locations
if [ -n "${WORKSPACE_FOLDER}" ]; then
    WORKSPACE_ROOT="${WORKSPACE_FOLDER}"
elif [ -f "/workspaces/$(basename $(pwd))/pyproject.toml" ]; then
    WORKSPACE_ROOT="/workspaces/$(basename $(pwd))"
elif [ -f "$(pwd)/pyproject.toml" ]; then
    WORKSPACE_ROOT="$(pwd)"
else
    echo "❌ Could not detect workspace root. Expected to find pyproject.toml"
    exit 1
fi

DEVCONTAINER_DIR="$WORKSPACE_ROOT/.devcontainer"
VSCODE_DIR="$WORKSPACE_ROOT/.vscode"

echo "🔧 Setting up VS Code workspace configuration..."
echo "📁 Workspace root: $WORKSPACE_ROOT"

# Create .vscode directory if it doesn't exist
mkdir -p "$VSCODE_DIR"

# Copy VS Code configurations from devcontainer .vscode directory
if [ -d "$DEVCONTAINER_DIR/.vscode" ]; then
    echo "📂 Copying VS Code settings from .devcontainer/.vscode to workspace"
    cp -r "$DEVCONTAINER_DIR/.vscode/"* "$VSCODE_DIR/"
fi

echo "🎉 VS Code workspace configuration complete!"
echo "📝 Note: .vscode/ is ignored in git - these settings are container-only"

# Make install to ensure dependencies are set up
echo "📦 Installing dependencies..."
make install
