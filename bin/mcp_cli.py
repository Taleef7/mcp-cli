#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP CLI - Command Line Interface for the Model Context Protocol

This CLI allows you to manage MCP servers and interact with them using OpenAI's GPT-3.5 Turbo.
It provides commands to:
1. Add/remove/list MCP servers
2. Run queries against the servers using the LLM
3. Manage configurations
"""

from mcp_cli.cli import main

if __name__ == "__main__":
    main() 