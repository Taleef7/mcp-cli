# MCP CLI API Reference

This document provides comprehensive documentation for the RESTful API server of the MCP CLI (Model Context Protocol Command Line Interface). The API server allows you to access MCP CLI functionality via HTTP requests from any client.

## Overview

The MCP CLI API server provides a RESTful interface to manage MCP servers, run queries against them, discover available tools, and handle configuration. This enables integration with various clients including web applications, mobile apps, and other services.

## Getting Started

### Starting the API Server

```bash
# Using the installed package
mcp-server

# With custom host and port
mcp-server --host 127.0.0.1 --port 8080

# In debug mode
mcp-server --debug
```

By default, the server listens on `0.0.0.0:5000`.

### API Base URL

All endpoints are prefixed with `/api`:

```
http://{host}:{port}/api/
```

## Authentication

Currently, the API does not include authentication mechanisms. If deployed in a production environment, it's recommended to implement appropriate authentication.

## Response Format

All API responses use JSON format with the following structure:

For successful responses:
```json
{
  "status": "success",
  "message": "Optional success message",
  "data_field": "Response data varies by endpoint"
}
```

For error responses:
```json
{
  "error": "Error message describing what went wrong"
}
```

Error responses also include an appropriate HTTP status code (400, 404, 500, etc.).

## Endpoints Reference

### Status Endpoint

#### Get API Status

`GET /api/status`

Returns the current status of the API server.

**Response**:
```json
{
  "status": "ok",
  "service": "mcp-cli-api",
  "version": "0.1.0"
}
```

### Servers Endpoints

#### List All Servers

`GET /api/servers`

Returns a list of all configured MCP servers.

**Response**:
```json
{
  "servers": [
    {
      "name": "playwright",
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "env": {"DISPLAY": ":1"}
    },
    {
      "name": "airbnb",
      "command": "npx",
      "args": ["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
      "env": {}
    }
  ]
}
```

#### Get Server Details

`GET /api/servers/{name}`

Returns details for a specific MCP server.

**URL Parameters**:
- `name` (required): Name of the server to retrieve

**Response (Success)**:
```json
{
  "name": "playwright",
  "command": "npx",
  "args": ["@playwright/mcp@latest"],
  "env": {"DISPLAY": ":1"}
}
```

**Response (Error)**:
```json
{
  "error": "Server 'playwright' not found",
  "available_servers": ["airbnb", "filesystem"]
}
```

#### Add New Server

`POST /api/servers`

Creates a new MCP server configuration.

**Request Body**:
```json
{
  "name": "playwright",
  "command": "npx",
  "args": ["@playwright/mcp@latest"],
  "env": {"DISPLAY": ":1"}
}
```

**Parameters**:
- `name` (required): Unique name for the server
- `command` (required): Command to run the server
- `args` (optional): Command line arguments as an array
- `env` (optional): Environment variables as key-value pairs

**Response (Success)**:
```json
{
  "status": "success",
  "message": "Server 'playwright' added successfully"
}
```

**Response (Error)**:
```json
{
  "error": "Server name is required"
}
```

#### Update Server

`PUT /api/servers/{name}`

Updates an existing MCP server configuration.

**URL Parameters**:
- `name` (required): Name of the server to update

**Request Body**:
```json
{
  "command": "npx",
  "args": ["@playwright/mcp@latest", "--headless"],
  "env": {"DISPLAY": ":1", "DEBUG": "pw:api"}
}
```

**Parameters**:
- `command` (optional): New command to run the server
- `args` (optional): New command line arguments as an array
- `env` (optional): New environment variables as key-value pairs

**Response (Success)**:
```json
{
  "status": "success",
  "message": "Server 'playwright' updated successfully"
}
```

**Response (Error)**:
```json
{
  "error": "Server 'playwright' not found",
  "available_servers": ["airbnb", "filesystem"]
}
```

#### Remove Server

`DELETE /api/servers/{name}`

Removes an MCP server configuration.

**URL Parameters**:
- `name` (required): Name of the server to remove

**Response (Success)**:
```json
{
  "status": "success", 
  "message": "Server 'playwright' removed successfully"
}
```

**Response (Error)**:
```json
{
  "error": "Server 'playwright' not found",
  "available_servers": ["airbnb", "filesystem"]
}
```

### Query Endpoint

#### Run Query

`POST /api/query`

Executes a query against an MCP server.

**Request Body**:
```json
{
  "server": "playwright",
  "query": "Find the best restaurants in San Francisco",
  "model": "gpt-3.5-turbo"
}
```

**Parameters**:
- `server` (required): Name of the MCP server to query
- `query` (required): The query to execute
- `model` (optional): The OpenAI model to use (default: "gpt-3.5-turbo")

**Response (Success)**:
```json
{
  "status": "success",
  "result": "Here are some of the best restaurants in San Francisco: ..."
}
```

**Response (Error)**:
```json
{
  "error": "Server 'playwright' not found"
}
```

### Tools Endpoint

#### List Server Tools

`GET /api/servers/{name}/tools`

Returns a list of tools provided by an MCP server.

**URL Parameters**:
- `name` (required): Name of the server to query for tools

**Query Parameters**:
- `model` (optional): The OpenAI model to use for tool discovery (default: "gpt-3.5-turbo")

**Response (Success)**:
```json
{
  "status": "success",
  "tools": [
    {
      "name": "search_google",
      "description": "Search Google for a query",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "Search query"
          }
        },
        "required": ["query"]
      }
    },
    {
      "name": "visit_page",
      "description": "Visit a webpage and extract its content",
      "parameters": {
        "type": "object",
        "properties": {
          "url": {
            "type": "string",
            "description": "URL to visit"
          },
          "takeScreenshot": {
            "type": "boolean",
            "description": "Whether to take a screenshot"
          }
        },
        "required": ["url"]
      }
    }
  ]
}
```

**Response (Error)**:
```json
{
  "error": "Server 'playwright' not found",
  "available_servers": ["airbnb", "filesystem"]
}
```

### Configuration Endpoints

#### Export Configuration

`POST /api/config/export`

Exports the current configuration to a file.

**Request Body**:
```json
{
  "filepath": "/path/to/config.json"
}
```

**Parameters**:
- `filepath` (required): Path where to save the configuration file

**Response (Success)**:
```json
{
  "status": "success",
  "message": "Configuration exported to /path/to/config.json"
}
```

**Response (Error)**:
```json
{
  "error": "Failed to write to file: Permission denied"
}
```

#### Import Configuration

`POST /api/config/import`

Imports configuration from a file.

**Request Body**:
```json
{
  "filepath": "/path/to/config.json"
}
```

**Parameters**:
- `filepath` (required): Path to the configuration file to import

**Response (Success)**:
```json
{
  "status": "success",
  "message": "Configuration imported from /path/to/config.json"
}
```

**Response (Error)**:
```json
{
  "error": "File '/path/to/config.json' not found"
}
```

## Error Handling

The API uses standard HTTP status codes:

- `200 OK`: Request succeeded
- `400 Bad Request`: Invalid request (missing parameters, etc.)
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

All error responses include an `error` field with a description of the problem.

## Client Integration Examples

### cURL

#### List All Servers
```bash
curl -X GET http://localhost:5000/api/servers
```

#### Add a New Server
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

### JavaScript/Node.js

```javascript
// Function to run a query against an MCP server
async function runQuery(server, query, model = "gpt-3.5-turbo") {
  const response = await fetch('http://localhost:5000/api/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      server,
      query,
      model,
    }),
  });
  
  const data = await response.json();
  if (data.error) {
    throw new Error(data.error);
  }
  
  return data.result;
}

// Function to add a new MCP server
async function addServer(name, command, args = [], env = {}) {
  const response = await fetch('http://localhost:5000/api/servers', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name,
      command,
      args,
      env,
    }),
  });
  
  const data = await response.json();
  if (data.error) {
    throw new Error(data.error);
  }
  
  return data;
}

// Usage examples
async function examples() {
  try {
    // Add a server
    await addServer('playwright', 'npx', ['@playwright/mcp@latest'], { DISPLAY: ':1' });
    
    // Run a query
    const result = await runQuery('playwright', 'Find the best restaurants in San Francisco');
    console.log(result);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

examples();
```

### Python

```python
import requests
import json

BASE_URL = "http://localhost:5000/api"

def list_servers():
    """List all configured MCP servers."""
    response = requests.get(f"{BASE_URL}/servers")
    return response.json()

def add_server(name, command, args=None, env=None):
    """Add a new MCP server."""
    if args is None:
        args = []
    if env is None:
        env = {}
        
    data = {
        "name": name,
        "command": command,
        "args": args,
        "env": env
    }
    
    response = requests.post(
        f"{BASE_URL}/servers",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data)
    )
    
    return response.json()

def run_query(server, query, model="gpt-3.5-turbo"):
    """Run a query against an MCP server."""
    data = {
        "server": server,
        "query": query,
        "model": model
    }
    
    response = requests.post(
        f"{BASE_URL}/query",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data)
    )
    
    return response.json()

# Usage example
if __name__ == "__main__":
    # List all servers
    servers = list_servers()
    print(f"Configured servers: {', '.join([s['name'] for s in servers['servers']])}")
    
    # Add a new server
    result = add_server(
        "playwright",
        "npx",
        ["@playwright/mcp@latest"],
        {"DISPLAY": ":1"}
    )
    print(f"Add server result: {result}")
    
    # Run a query
    result = run_query("playwright", "Find the best restaurants in San Francisco")
    print(f"Query result: {result['result']}") 