#!/usr/bin/env python3
"""
Main entry point for the MCP CLI package.
This allows the package to be executed with: python -m mcp_cli
"""

# Use the GUI as the main entry point instead of the CLI
from mcp_cli.gui.app import main

if __name__ == "__main__":
    main() 