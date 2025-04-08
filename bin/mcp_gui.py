#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP GUI - Graphical User Interface for the Model Context Protocol

This GUI allows you to manage MCP servers and interact with them using OpenAI's models.
It provides a user-friendly interface to:
1. Add/remove/list MCP servers
2. Run queries against the servers using the LLM
3. Manage configurations
4. View tools available from the servers
"""

from mcp_cli.gui.app import main

if __name__ == "__main__":
    main() 