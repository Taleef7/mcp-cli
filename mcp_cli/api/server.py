#!/usr/bin/env python3
"""
RESTful API server for MCP CLI.
This module provides a Flask-based HTTP server exposing 
the MCP CLI functionality through API endpoints.
"""

import os
import json
import logging
import asyncio
import argparse
from typing import Dict, List, Optional, Any

from flask import Flask, request, jsonify
from flask_cors import CORS

# Import MCP CLI core functions
from mcp_cli.core import (
    load_config, save_config, list_servers, run_query,
    add_server, remove_server, export_config, import_config,
    get_server_info, list_tools, DEFAULT_MODEL
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Helper function to run async functions in Flask routes
def run_async(coroutine):
    """Run an async function in a Flask route."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coroutine)
    finally:
        loop.close()

# Status endpoint
@app.route('/api/status', methods=['GET'])
def get_status():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'service': 'mcp-cli-api',
        'version': '0.1.0'
    })

# Servers endpoints
@app.route('/api/servers', methods=['GET'])
def get_servers():
    """List all configured MCP servers."""
    config = load_config()
    servers = config.get("mcpServers", {})
    return jsonify({
        'servers': [
            {
                'name': name,
                'command': server_config.get('command', ''),
                'args': server_config.get('args', []),
                'env': server_config.get('env', {})
            }
            for name, server_config in servers.items()
        ]
    })

@app.route('/api/servers/<name>', methods=['GET'])
def get_server(name):
    """Get information about a specific MCP server."""
    config = load_config()
    servers = config.get("mcpServers", {})
    
    if name not in servers:
        return jsonify({
            'error': f"Server '{name}' not found",
            'available_servers': list(servers.keys())
        }), 404
    
    server_config = servers[name]
    return jsonify({
        'name': name,
        'command': server_config.get('command', ''),
        'args': server_config.get('args', []),
        'env': server_config.get('env', {})
    })

@app.route('/api/servers', methods=['POST'])
def create_server():
    """Add a new MCP server."""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    name = data.get('name')
    command = data.get('command')
    args = data.get('args', [])
    env = data.get('env')
    
    if not name:
        return jsonify({'error': 'Server name is required'}), 400
    if not command:
        return jsonify({'error': 'Command is required'}), 400
    
    try:
        add_server(name, command, args, env)
        return jsonify({
            'status': 'success',
            'message': f"Server '{name}' added successfully"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/servers/<name>', methods=['PUT'])
def update_server(name):
    """Update an existing MCP server."""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    command = data.get('command')
    args = data.get('args')
    env = data.get('env')
    
    if not command and not args and not env:
        return jsonify({'error': 'At least one of command, args, or env must be provided'}), 400
    
    try:
        # Load current configuration
        config = load_config()
        servers = config.get("mcpServers", {})
        
        if name not in servers:
            return jsonify({
                'error': f"Server '{name}' not found",
                'available_servers': list(servers.keys())
            }), 404
        
        # Update server configuration
        if command:
            servers[name]['command'] = command
        if args:
            servers[name]['args'] = args
        if env:
            servers[name]['env'] = env
        
        # Save updated configuration
        save_config(config)
        
        return jsonify({
            'status': 'success',
            'message': f"Server '{name}' updated successfully"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/servers/<name>', methods=['DELETE'])
def delete_server(name):
    """Remove an MCP server."""
    config = load_config()
    servers = config.get("mcpServers", {})
    
    if name not in servers:
        return jsonify({
            'error': f"Server '{name}' not found",
            'available_servers': list(servers.keys())
        }), 404
    
    try:
        remove_server(name)
        return jsonify({
            'status': 'success',
            'message': f"Server '{name}' removed successfully"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Query endpoints
@app.route('/api/query', methods=['POST'])
def execute_query():
    """Run a query against an MCP server."""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    server_name = data.get('server')
    query = data.get('query')
    model = data.get('model', DEFAULT_MODEL)
    
    if not server_name:
        return jsonify({'error': 'Server name is required'}), 400
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    try:
        result = run_async(run_query(server_name, query, model, True))
        return jsonify({
            'status': 'success',
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Tools endpoints
@app.route('/api/servers/<name>/tools', methods=['GET'])
def get_tools(name):
    """List tools provided by an MCP server."""
    model = request.args.get('model', DEFAULT_MODEL)
    
    config = load_config()
    servers = config.get("mcpServers", {})
    
    if name not in servers:
        return jsonify({
            'error': f"Server '{name}' not found",
            'available_servers': list(servers.keys())
        }), 404
    
    try:
        # Call the tools listing function
        result = run_async(list_tools(name, model, True))
        logger.info(f"Tools result from server '{name}': {result}")
        
        # Parse the text result into a structured format
        # This is a simple parsing, you may need to improve it
        tools = []
        current_tool = None
        
        for line in result.split('\n'):
            if line.startswith('• '):
                if current_tool:
                    tools.append(current_tool)
                
                current_tool = {
                    'name': line[2:].strip(),
                    'description': '',
                    'parameters': {}
                }
            elif current_tool and line.strip().startswith('Description:'):
                current_tool['description'] = line.replace('Description:', '').strip()
            elif current_tool and line.strip().startswith('Parameters:'):
                # Try to parse parameters as JSON
                try:
                    params_text = line.replace('Parameters:', '').strip()
                    # Combine with next lines if it's only the start of JSON
                    if params_text.startswith('{') and not params_text.endswith('}'):
                        params_lines = []
                        for i, next_line in enumerate(result.split('\n')[result.split('\n').index(line) + 1:]):
                            params_lines.append(next_line.strip())
                            combined = params_text + ' ' + ' '.join(params_lines)
                            try:
                                json.loads(combined)
                                params_text = combined
                                break
                            except:
                                continue
                    
                    current_tool['parameters'] = json.loads(params_text)
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse parameters: {params_text}")
                    current_tool['parameters'] = {"error": "Failed to parse parameters"}
        
        # Add the last tool if there is one
        if current_tool:
            tools.append(current_tool)
        
        return jsonify({
            'status': 'success',
            'tools': tools
        })
    except Exception as e:
        logger.error(f"Error getting tools: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Configuration endpoints
@app.route('/api/config/export', methods=['POST'])
def export_configuration():
    """Export the configuration to a file."""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    filepath = data.get('filepath')
    
    if not filepath:
        return jsonify({'error': 'File path is required'}), 400
    
    try:
        export_config(filepath)
        return jsonify({
            'status': 'success',
            'message': f"Configuration exported to {filepath}"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config/import', methods=['POST'])
def import_configuration():
    """Import configuration from a file."""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    filepath = data.get('filepath')
    
    if not filepath:
        return jsonify({'error': 'File path is required'}), 400
    
    if not os.path.exists(filepath):
        return jsonify({'error': f"File '{filepath}' not found"}), 404
    
    try:
        import_config(filepath)
        return jsonify({
            'status': 'success',
            'message': f"Configuration imported from {filepath}"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="MCP CLI API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the server on")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    return parser.parse_args()

def main():
    """Main entry point for the API server."""
    args = parse_args()
    logger.info(f"Starting MCP CLI API server on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main() 