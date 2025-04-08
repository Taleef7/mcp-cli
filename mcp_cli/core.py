"""
Core functionality for the MCP CLI.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

import dotenv
from langchain_openai import ChatOpenAI

from mcp_use import MCPAgent, MCPClient

# Get the project root directory
# Try to find the project root by first checking if we're in development mode
def get_project_root():
    """Get the absolute path to the project root directory."""
    # First check if we're running from the project directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(current_dir, '..'))
    
    # Check if this looks like the project directory (has setup.py)
    if os.path.exists(os.path.join(project_dir, 'setup.py')):
        return project_dir
    
    # If we're running from an installed package, use the current working directory
    cwd = os.getcwd()
    if os.path.basename(cwd) == 'mcp-cli-project':
        return cwd
    
    # Fallback to checking if 'mcp-cli-project' directory exists in the current path
    mcp_cli_dir = os.path.join(cwd, 'mcp-cli-project')
    if os.path.exists(mcp_cli_dir) and os.path.isdir(mcp_cli_dir):
        return mcp_cli_dir
    
    # Last resort, check parent directory
    parent_dir = os.path.abspath(os.path.join(cwd, '..'))
    if os.path.basename(parent_dir) == 'mcp-cli-project':
        return parent_dir
    
    # If all else fails, create a directory in the current working directory
    mcp_cli_dir = os.path.join(cwd, 'mcp-cli-project')
    if not os.path.exists(mcp_cli_dir):
        os.makedirs(mcp_cli_dir)
    return mcp_cli_dir

# Constants
PROJECT_ROOT = get_project_root()
DEFAULT_CONFIG_DIR = os.path.join(PROJECT_ROOT, 'config')
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_DIR, 'config.json')
DEFAULT_MODEL = "gpt-3.5-turbo"

# Backup constants (for compatibility with existing installations)
LEGACY_CONFIG_DIR = os.path.expanduser("~/.mcp-cli")
LEGACY_CONFIG_FILE = os.path.join(LEGACY_CONFIG_DIR, "config.json")

def ensure_config_dir():
    """Ensure the configuration directory exists."""
    if not os.path.exists(DEFAULT_CONFIG_DIR):
        os.makedirs(DEFAULT_CONFIG_DIR)
    
    if not os.path.exists(DEFAULT_CONFIG_FILE):
        # Check if there's a legacy config file we should migrate
        if os.path.exists(LEGACY_CONFIG_FILE):
            try:
                with open(LEGACY_CONFIG_FILE, "r") as f:
                    legacy_config = json.load(f)
                
                with open(DEFAULT_CONFIG_FILE, "w") as f:
                    json.dump(legacy_config, f, indent=2)
                
                print(f"Migrated configuration from {LEGACY_CONFIG_FILE} to {DEFAULT_CONFIG_FILE}")
                return
            except Exception as e:
                print(f"Failed to migrate legacy configuration: {e}")
        
        # If no legacy config or migration failed, create a new empty config
        with open(DEFAULT_CONFIG_FILE, "w") as f:
            json.dump({"mcpServers": {}}, f, indent=2)

def load_config() -> Dict[str, Any]:
    """Load the configuration file."""
    ensure_config_dir()
    with open(DEFAULT_CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config: Dict[str, Any]):
    """Save the configuration file."""
    ensure_config_dir()
    with open(DEFAULT_CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def list_servers():
    """List all configured MCP servers."""
    config = load_config()
    servers = config.get("mcpServers", {})
    
    if not servers:
        print("No MCP servers configured.")
        print("Use 'mcp_cli.py add-server' to add a new server.")
        return
    
    print("Configured MCP servers:")
    for name, server_config in servers.items():
        command = server_config.get("command", "N/A")
        args = " ".join(server_config.get("args", []))
        print(f"  - {name}: {command} {args}")

async def run_query(server_name: str, query: str, model: str = DEFAULT_MODEL, return_result: bool = False):
    """Run a query against a specified MCP server.
    
    Args:
        server_name: Name of the server to use
        query: Query to run
        model: OpenAI model to use
        return_result: If True, returns the result instead of printing it
        
    Returns:
        If return_result is True, returns the result as a string,
        otherwise prints the result and returns None.
    """
    config = load_config()
    servers = config.get("mcpServers", {})
    
    if server_name not in servers:
        message = f"Error: Server '{server_name}' not found."
        message += "\nAvailable servers:"
        for name in servers.keys():
            message += f"\n  - {name}"
        if return_result:
            return message
        print(message)
        return
    
    # Create a temporary config with just the selected server
    temp_config = {"mcpServers": {server_name: servers[server_name]}}
    
    # Load environment variables
    dotenv.load_dotenv()
    
    # Check if OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        message = "Error: OPENAI_API_KEY environment variable not set."
        message += "\nPlease set it in your .env file or as an environment variable."
        if return_result:
            return message
        print(message)
        return
    
    result_output = []
    def capture_print(text):
        if return_result:
            result_output.append(text)
        print(text)
    
    try:
        capture_print(f"Connecting to MCP server '{server_name}'...")
        client = MCPClient.from_dict(temp_config)
        
        capture_print(f"Using OpenAI model '{model}'...")
        llm = ChatOpenAI(model=model)
        
        capture_print("Initializing agent...")
        agent = MCPAgent(llm=llm, client=client, max_steps=30)
        
        capture_print(f"Running query: {query}")
        capture_print("Processing (this may take a moment)...")
        result = await agent.run(query, max_steps=30)
        
        capture_print("\n--- Result ---")
        capture_print(result)
        capture_print("-------------")
        
        if return_result:
            return result
        
    except Exception as e:
        message = f"Error: {e}"
        if return_result:
            return message
        print(message)
    finally:
        # Clean up
        if 'client' in locals() and hasattr(client, 'sessions') and client.sessions:
            capture_print("Closing sessions...")
            await client.close_all_sessions()

def add_server(name: str, command: str, args: List[str], env: Optional[Dict[str, str]] = None):
    """Add a new MCP server configuration."""
    config = load_config()
    
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    server_config = {
        "command": command,
        "args": args
    }
    
    if env:
        server_config["env"] = env
    
    config["mcpServers"][name] = server_config
    save_config(config)
    
    print(f"MCP server '{name}' added successfully.")

def remove_server(name: str):
    """Remove an MCP server configuration."""
    config = load_config()
    
    if "mcpServers" not in config or name not in config["mcpServers"]:
        print(f"Error: Server '{name}' not found.")
        return
    
    del config["mcpServers"][name]
    save_config(config)
    
    print(f"MCP server '{name}' removed successfully.")

def export_config(filepath: str):
    """Export the configuration to a file."""
    config = load_config()
    
    with open(filepath, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"Configuration exported to {filepath}")

def import_config(filepath: str):
    """Import configuration from a file."""
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return
    
    try:
        with open(filepath, "r") as f:
            config = json.load(f)
        
        save_config(config)
        print(f"Configuration imported from {filepath}")
    except json.JSONDecodeError:
        print(f"Error: File '{filepath}' is not a valid JSON file.")

def get_server_info(server_name: str):
    """Get detailed information about a server."""
    config = load_config()
    servers = config.get("mcpServers", {})
    
    if server_name not in servers:
        print(f"Error: Server '{server_name}' not found.")
        return
    
    server_config = servers[server_name]
    
    print(f"Server: {server_name}")
    print(f"Command: {server_config.get('command', 'N/A')}")
    print(f"Arguments: {' '.join(server_config.get('args', []))}")
    
    if "env" in server_config:
        print("Environment variables:")
        for key, value in server_config["env"].items():
            print(f"  {key}={value}")

async def list_tools(server_name: str, model: str = DEFAULT_MODEL, return_result: bool = False):
    """Connect to a server and list its available tools.
    
    Args:
        server_name: Name of the server to use
        model: OpenAI model to use
        return_result: If True, returns the result instead of printing it
        
    Returns:
        If return_result is True, returns the result as a string,
        otherwise prints the result and returns None.
    """
    config = load_config()
    servers = config.get("mcpServers", {})
    
    if server_name not in servers:
        message = f"Error: Server '{server_name}' not found."
        if return_result:
            return message
        print(message)
        return
    
    # Create a temporary config with just the selected server
    temp_config = {"mcpServers": {server_name: servers[server_name]}}
    
    # Load environment variables
    dotenv.load_dotenv()

    result_output = []
    def capture_print(text):
        if return_result:
            result_output.append(text)
        print(text)
    
    try:
        capture_print(f"Connecting to MCP server '{server_name}'...")
        client = MCPClient.from_dict(temp_config)
        
        # Create a dummy LLM (needed to initialize the agent)
        llm = ChatOpenAI(model=model)
        
        capture_print("Initializing agent to discover tools...")
        agent = MCPAgent(llm=llm, client=client)
        
        # Initialize to discover tools
        await agent.initialize()
        
        # Get session and its connector (which has tool info)
        if client.sessions:
            session = next(iter(client.sessions.values()))
            connector = session.connector
            
            if hasattr(connector, 'tools') and connector.tools:
                capture_print(f"\nTools available from '{server_name}':")
                for tool in connector.tools:
                    capture_print(f"\n• {tool.name}")
                    if hasattr(tool, 'description') and tool.description:
                        capture_print(f"  Description: {tool.description}")
                    if hasattr(tool, 'input_schema') and tool.input_schema:
                        capture_print(f"  Parameters: {json.dumps(tool.input_schema, indent=2)}")
            else:
                capture_print(f"No tools found in server '{server_name}'")
        else:
            capture_print(f"Failed to connect to server '{server_name}'")
            
        if return_result:
            return "\n".join(result_output)
            
    except Exception as e:
        message = f"Error connecting to server or listing tools: {e}"
        if return_result:
            return message
        print(message)
    finally:
        # Clean up
        if 'client' in locals() and hasattr(client, 'sessions') and client.sessions:
            await client.close_all_sessions() 