"""
MCP CLI - GUI Interface for the Model Context Protocol

This module provides a graphical user interface for interacting with MCP servers.
The CLI functionality is still available as a submodule.
"""

__version__ = "0.1.0"

# Make the GUI functionality directly available
from mcp_cli.gui.app import main, MCPCliGui 