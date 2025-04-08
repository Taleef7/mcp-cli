# MCP CLI API Quickstart Guide

This guide will help you quickly get started with the MCP CLI API server, including installation, basic setup, and common operations.

## Installation

### Prerequisites

- Python 3.8+
- pip
- An OpenAI API key

### Installing MCP CLI

Install the MCP CLI package, which includes the API server:

```bash
# From PyPI
pip install mcp-cli

# Or from source
git clone https://github.com/your-org/mcp-cli-project.git
cd mcp-cli-project
pip install -e .
```

### Setting Up Your OpenAI API Key

Create a `.env` file in your working directory with your OpenAI API key:

```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

Alternatively, set it as an environment variable:

```bash
export OPENAI_API_KEY=your_api_key_here
```

## Starting the API Server

Start the API server with default settings (host 0.0.0.0, port 5000):

```bash
mcp-server
```

Customize host and port:

```bash
mcp-server --host 127.0.0.1 --port 8080
```

Run in debug mode for development:

```bash
mcp-server --debug
```

The server will start and display a message like:
```
Starting MCP CLI API server on 0.0.0.0:5000
 * Serving Flask app...
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

## Quick API Examples

Here are some quick examples to help you get started with the API.

### Check API Status

```bash
curl -X GET http://localhost:5000/api/status
```

Expected response:
```json
{
  "status": "ok",
  "service": "mcp-cli-api",
  "version": "0.1.0"
}
```

### Manage MCP Servers

#### Add a New Server

Add the Playwright MCP server for web browsing:

```bash
curl -X POST http://localhost:5000/api/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "playwright",
    "command": "npx",
    "args": ["@playwright/mcp@latest"],
    "env": {"DISPLAY": ":1"}
  }'
```

#### List All Servers

```bash
curl -X GET http://localhost:5000/api/servers
```

#### Get Information about a Specific Server

```bash
curl -X GET http://localhost:5000/api/servers/playwright
```

#### Update a Server

```bash
curl -X PUT http://localhost:5000/api/servers/playwright \
  -H "Content-Type: application/json" \
  -d '{
    "args": ["@playwright/mcp@latest", "--headless"]
  }'
```

#### Remove a Server

```bash
curl -X DELETE http://localhost:5000/api/servers/playwright
```

### Working with MCP Servers

#### Run a Query

```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "server": "playwright",
    "query": "Find the best restaurants in San Francisco",
    "model": "gpt-3.5-turbo"
  }'
```

#### List Available Tools

```bash
curl -X GET http://localhost:5000/api/servers/playwright/tools
```

### Configuration Management

#### Export Configuration

```bash
curl -X POST http://localhost:5000/api/config/export \
  -H "Content-Type: application/json" \
  -d '{
    "filepath": "/path/to/config.json"
  }'
```

#### Import Configuration

```bash
curl -X POST http://localhost:5000/api/config/import \
  -H "Content-Type: application/json" \
  -d '{
    "filepath": "/path/to/config.json"
  }'
```

## Using with JavaScript/Node.js

Here's a simple Node.js script to interact with the API:

```javascript
const API_URL = 'http://localhost:5000/api';

// Helper function for API requests
async function apiRequest(path, method = 'GET', body = null) {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };
  
  if (body) {
    options.body = JSON.stringify(body);
  }
  
  const response = await fetch(`${API_URL}${path}`, options);
  return response.json();
}

// Common operations
async function listServers() {
  return apiRequest('/servers');
}

async function addServer(name, command, args = [], env = {}) {
  return apiRequest('/servers', 'POST', { name, command, args, env });
}

async function runQuery(server, query, model = 'gpt-3.5-turbo') {
  return apiRequest('/query', 'POST', { server, query, model });
}

// Example usage
async function main() {
  try {
    // Add a Playwright server
    await addServer('playwright', 'npx', ['@playwright/mcp@latest'], { DISPLAY: ':1' });
    console.log('Server added successfully');
    
    // List all servers
    const servers = await listServers();
    console.log('Configured servers:', servers);
    
    // Run a query
    const result = await runQuery('playwright', 'What is the weather in New York?');
    console.log('Query result:', result);
  } catch (error) {
    console.error('Error:', error);
  }
}

main();
```

## Using with Python

Here's a simple Python script to interact with the API:

```python
import requests
import json

API_URL = 'http://localhost:5000/api'

def api_request(path, method='GET', data=None):
    """Helper function for API requests."""
    url = f"{API_URL}{path}"
    headers = {'Content-Type': 'application/json'}
    
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, data=json.dumps(data))
    elif method == 'PUT':
        response = requests.put(url, headers=headers, data=json.dumps(data))
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")
    
    return response.json()

# Common operations
def list_servers():
    """List all configured MCP servers."""
    return api_request('/servers')

def add_server(name, command, args=None, env=None):
    """Add a new MCP server."""
    if args is None:
        args = []
    if env is None:
        env = {}
    
    return api_request('/servers', 'POST', {
        'name': name,
        'command': command,
        'args': args,
        'env': env
    })

def run_query(server, query, model='gpt-3.5-turbo'):
    """Run a query against an MCP server."""
    return api_request('/query', 'POST', {
        'server': server,
        'query': query,
        'model': model
    })

# Example usage
if __name__ == '__main__':
    try:
        # Add a Playwright server
        add_server('playwright', 'npx', ['@playwright/mcp@latest'], {'DISPLAY': ':1'})
        print('Server added successfully')
        
        # List all servers
        servers = list_servers()
        print('Configured servers:', servers)
        
        # Run a query
        result = run_query('playwright', 'What is the weather in New York?')
        print('Query result:', result)
    except Exception as e:
        print(f'Error: {str(e)}')
```

## Common Operations

### Setting Up Multiple MCP Servers

Here's how to set up a few common MCP servers:

#### Playwright (Web Browsing)

```bash
curl -X POST http://localhost:5000/api/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "playwright",
    "command": "npx",
    "args": ["@playwright/mcp@latest"],
    "env": {"DISPLAY": ":1"}
  }'
```

#### Airbnb (Accommodation Search)

```bash
curl -X POST http://localhost:5000/api/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "airbnb",
    "command": "npx",
    "args": ["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
    "env": {}
  }'
```

#### Filesystem (Local File Access)

```bash
curl -X POST http://localhost:5000/api/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "filesystem",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/directory"],
    "env": {}
  }'
```

## Troubleshooting

### API Key Issues

If you get errors about the OpenAI API key:
- Ensure your `.env` file is in the correct location
- Check that the API key is valid and has the necessary permissions
- Try setting the API key as an environment variable instead

### Connection Errors

If you cannot connect to the API server:
- Make sure the server is running
- Verify the host and port settings
- Check if any firewall is blocking connections

### MCP Server Issues

If you get errors when running queries:
- Make sure the MCP server is installed and accessible
- For NPM-based servers, try installing them globally first
- Check the server-specific documentation for any additional requirements

## Next Steps

Once you're comfortable with the basics, check out:
- [API Reference](README.md) for detailed documentation on all endpoints
- [Technical Documentation](TECHNICAL_DOCS.md) for implementation details
- [MCP Protocol Documentation](https://github.com/modelcontextprotocol/docs) for more information about the Model Context Protocol 