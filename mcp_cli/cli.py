"""
Command line interface functionality for MCP CLI.
"""

import argparse
import asyncio
from typing import Dict, List, Optional

from mcp_cli.core import (
    DEFAULT_MODEL,
    add_server,
    export_config,
    get_server_info,
    import_config,
    list_servers,
    list_tools,
    remove_server,
    run_query,
)

def create_parser():
    """Create the command line argument parser."""
    parser = argparse.ArgumentParser(description="MCP CLI - Command Line Interface for the Model Context Protocol")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List servers command
    list_parser = subparsers.add_parser("list", help="List all configured MCP servers")
    
    # Run query command
    run_parser = subparsers.add_parser("run", help="Run a query against an MCP server")
    run_parser.add_argument("server", help="Server name to use")
    run_parser.add_argument("query", help="Query to run")
    run_parser.add_argument("--model", default=DEFAULT_MODEL, help=f"OpenAI model to use (default: {DEFAULT_MODEL})")
    
    # Add server command
    add_parser = subparsers.add_parser("add", help="Add a new MCP server")
    add_parser.add_argument("name", help="Server name")
    add_parser.add_argument("command", help="Command to run the server (e.g., npx)")
    add_parser.add_argument("args", nargs="+", help="Arguments for the command")
    add_parser.add_argument("--env", nargs="+", help="Environment variables in the format KEY=VALUE")
    
    # Remove server command
    remove_parser = subparsers.add_parser("remove", help="Remove an MCP server")
    remove_parser.add_argument("name", help="Server name to remove")
    
    # Export config command
    export_parser = subparsers.add_parser("export", help="Export configuration to a file")
    export_parser.add_argument("filepath", help="File path to export to")
    
    # Import config command
    import_parser = subparsers.add_parser("import", help="Import configuration from a file")
    import_parser.add_argument("filepath", help="File path to import from")
    
    # Server info command
    info_parser = subparsers.add_parser("info", help="Get detailed information about a server")
    info_parser.add_argument("server", help="Server name")
    
    # List tools command
    tools_parser = subparsers.add_parser("tools", help="List tools available from a server")
    tools_parser.add_argument("server", help="Server name")
    tools_parser.add_argument("--model", default=DEFAULT_MODEL, help=f"OpenAI model to use (default: {DEFAULT_MODEL})")
    
    return parser

async def main_async(args):
    """Asynchronous main function."""
    if args.command == "list":
        list_servers()
    elif args.command == "run":
        await run_query(args.server, args.query, args.model)
    elif args.command == "add":
        env_dict = None
        if args.env:
            env_dict = {}
            for env_var in args.env:
                key, value = env_var.split("=", 1)
                env_dict[key] = value
        add_server(args.name, args.command, args.args, env_dict)
    elif args.command == "remove":
        remove_server(args.name)
    elif args.command == "export":
        export_config(args.filepath)
    elif args.command == "import":
        import_config(args.filepath)
    elif args.command == "info":
        get_server_info(args.server)
    elif args.command == "tools":
        await list_tools(args.server, args.model)
    else:
        parser = create_parser()
        parser.print_help()

def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    asyncio.run(main_async(args))

if __name__ == "__main__":
    main() 