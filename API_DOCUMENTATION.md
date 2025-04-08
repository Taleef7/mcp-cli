# MCP CLI API Documentation

## Introduction

This documentation is intended for developers who plan to integrate the MCP CLI API into their applications. The service provides a RESTful interface for managing MCP (Model Context Protocol) servers and interacting with them via HTTP requests.

## General Information

**Base URL:** `http://[host]:[port]/api`  
**Content-Type:** `application/json`  
**Authentication:** Not required in the current version  
**Response Format:** JSON

## Starting the API Server

The server can be started in several ways:

```bash
# Using the installed mcp-server command
mcp-server --host 0.0.0.0 --port 8000 --debug

# Using Python directly
python -m mcp_cli.api.server --host 0.0.0.0 --port 8000 --debug

# Using Flask
export FLASK_APP=mcp_cli.api.server
export FLASK_DEBUG=1
flask run --host 0.0.0.0 --port 8000
```

### Startup Parameters

| Parameter | Type    | Default  | Description |
|-----------|---------|----------|-------------|
| `--host`  | String  | 0.0.0.0  | The IP address on which the server will listen for connections |
| `--port`  | Integer | 5000     | The port on which the server will listen for connections |
| `--debug` | Boolean | False    | Debug mode that provides detailed error information and automatically reloads the server when code changes are detected |

## API Endpoints

### 1. Server Status

#### `GET /api/status`

Returns the API server status.

**Request:**
```bash
curl -X GET http://localhost:8000/api/status
```

**Response:**
```json
{
  "status": "ok",
  "service": "mcp-cli-api",
  "version": "0.1.0"
}
```

**Status Codes:**
- `200 OK`: Request completed successfully

### 2. MCP Server Management

#### `GET /api/servers`

Returns a list of all configured MCP servers.

**Request:**
```bash
curl -X GET http://localhost:8000/api/servers
```

**Response:**
```json
{
  "servers": [
    {
      "name": "playwright",
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "env": {
        "DISPLAY": ":1"
      }
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

**Status Codes:**
- `200 OK`: Request completed successfully

#### `GET /api/servers/{name}`

Returns detailed information about a specific MCP server.

**URL Parameters:**
- `name` (required): The name of the MCP server

**Request:**
```bash
curl -X GET http://localhost:8000/api/servers/playwright
```

**Response:**
```json
{
  "name": "playwright",
  "command": "npx",
  "args": ["@playwright/mcp@latest"],
  "env": {
    "DISPLAY": ":1"
  }
}
```

**Status Codes:**
- `200 OK`: Request completed successfully
- `404 Not Found`: Server not found

#### `POST /api/servers`

Adds a new MCP server to the configuration.

**Body Parameters:**
- `name` (required): The name of the MCP server
- `command` (required): The command to start the MCP server
- `args` (optional): Array of arguments to pass to the command
- `env` (optional): Object of environment variables to set during command execution

**Request:**
```bash
curl -X POST http://localhost:8000/api/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "filesystem",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
    "env": {}
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Server 'filesystem' added successfully"
}
```

**Status Codes:**
- `200 OK`: Request completed successfully
- `400 Bad Request`: Missing or invalid parameters

#### `DELETE /api/servers/{name}`

Removes an MCP server from the configuration.

**URL Parameters:**
- `name` (required): The name of the MCP server to remove

**Request:**
```bash
curl -X DELETE http://localhost:8000/api/servers/filesystem
```

**Response:**
```json
{
  "status": "success",
  "message": "Server 'filesystem' removed successfully"
}
```

**Status Codes:**
- `200 OK`: Request completed successfully
- `404 Not Found`: Server not found

### 3. Query Execution

#### `POST /api/query`

Executes a query on a specific MCP server using an LLM model.

**Body Parameters:**
- `server` (required): The name of the MCP server to use
- `query` (required): The query to execute on the MCP server
- `model` (optional): The OpenAI model to use (default: "gpt-3.5-turbo")

**Request:**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "server": "airbnb",
    "query": "Find entire apartments in Rome, Italy for 2 adults from May 1 to May 7, 2025 with a price less than 160 euros per night",
    "model": "gpt-3.5-turbo"
  }'
```

**Response:**
```json
{
  "status": "success",
  "result": "I found several options for entire apartments in Rome, Italy for 2 adults from May 1 to May 7, 2025 with a price less than 160 euros per night. Here are some of them:\n\n1. [Vacation home in Flaminio](https://www.airbnb.com/rooms/1258700026649994455) - €137 per night (originally €163) - Total: €821\n2. [Apartment in Esquilino](https://www.airbnb.com/rooms/1354969952683182807) - €147 per night (originally €172) - Total: €878\n3. [Apartment in della Vittoria](https://www.airbnb.com/rooms/1118154891656189181) - €156 per night (originally €172) - Total: €931\n4. [Apartment in Appio Latino](https://www.airbnb.com/rooms/12621610) - €155 per night - Total: €928\n5. [Condo in Trionfale](https://www.airbnb.com/rooms/1383204233281708680) - €165 per night - Total: €986\n\nYou can view more options and book through [this link](https://www.airbnb.com/s/Rome%2C%20Italy/homes?checkin=2025-05-01&checkout=2025-05-07&adults=2&children=0&infants=0&pets=0&price_max=160)."
}
```

**Status Codes:**
- `200 OK`: Request completed successfully
- `400 Bad Request`: Missing or invalid parameters
- `404 Not Found`: Server not found
- `500 Internal Server Error`: Error during query execution

### 4. MCP Tools Management

#### `GET /api/servers/{name}/tools`

Returns a list of tools available on a specific MCP server.

**URL Parameters:**
- `name` (required): The name of the MCP server

**Query Parameters:**
- `model` (optional): The OpenAI model to use (default: "gpt-3.5-turbo")

**Request:**
```bash
curl -X GET "http://localhost:8000/api/servers/playwright/tools?model=gpt-3.5-turbo"
```

**Response:**
```json
{
  "status": "success",
  "tools": [
    {
      "name": "visit_page",
      "description": "Visit a webpage and extract its content",
      "parameters": {
        "properties": {
          "url": {
            "description": "URL to visit",
            "type": "string"
          },
          "takeScreenshot": {
            "description": "Whether to take a screenshot",
            "type": "boolean"
          }
        },
        "required": ["url"]
      }
    },
    {
      "name": "take_screenshot",
      "description": "Take a screenshot of the current page",
      "parameters": {
        "properties": {
          "random_string": {
            "description": "Dummy parameter for no-parameter tools",
            "type": "string"
          }
        },
        "required": ["random_string"]
      }
    }
  ]
}
```

**Status Codes:**
- `200 OK`: Request completed successfully
- `404 Not Found`: Server not found
- `500 Internal Server Error`: Error retrieving tools

### 5. Configuration Management

#### `POST /api/config/export`

Exports the current configuration to a file.

**Body Parameters:**
- `filepath` (required): The path of the file to export the configuration to

**Request:**
```bash
curl -X POST http://localhost:8000/api/config/export \
  -H "Content-Type: application/json" \
  -d '{
    "filepath": "/tmp/mcp-config.json"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Configuration exported to /tmp/mcp-config.json"
}
```

**Status Codes:**
- `200 OK`: Request completed successfully
- `400 Bad Request`: Missing or invalid parameters
- `500 Internal Server Error`: Error exporting configuration

#### `POST /api/config/import`

Imports configuration from a file.

**Body Parameters:**
- `filepath` (required): The path of the file to import the configuration from

**Request:**
```bash
curl -X POST http://localhost:8000/api/config/import \
  -H "Content-Type: application/json" \
  -d '{
    "filepath": "/tmp/mcp-config.json"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Configuration imported from /tmp/mcp-config.json"
}
```

**Status Codes:**
- `200 OK`: Request completed successfully
- `400 Bad Request`: Missing or invalid parameters
- `404 Not Found`: File not found
- `500 Internal Server Error`: Error importing configuration

## Integration Examples

### JavaScript/TypeScript Integration

#### Client Configuration
```javascript
class MCPCliClient {
  constructor(baseUrl = 'http://localhost:8000/api') {
    this.baseUrl = baseUrl;
  }

  async request(endpoint, method = 'GET', data = null) {
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, options);
    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || 'Unknown error');
    }

    return result;
  }

  // Server management
  async getServers() {
    return this.request('/servers');
  }

  async getServer(name) {
    return this.request(`/servers/${name}`);
  }

  async addServer(name, command, args = [], env = {}) {
    return this.request('/servers', 'POST', { name, command, args, env });
  }

  async removeServer(name) {
    return this.request(`/servers/${name}`, 'DELETE');
  }

  // Query execution
  async executeQuery(server, query, model = 'gpt-3.5-turbo') {
    return this.request('/query', 'POST', { server, query, model });
  }

  // Tools management
  async getTools(serverName, model = 'gpt-3.5-turbo') {
    return this.request(`/servers/${serverName}/tools?model=${model}`);
  }

  // Configuration management
  async exportConfig(filepath) {
    return this.request('/config/export', 'POST', { filepath });
  }

  async importConfig(filepath) {
    return this.request('/config/import', 'POST', { filepath });
  }
}
```

#### Usage Example
```javascript
async function main() {
  const client = new MCPCliClient('http://localhost:8000/api');

  try {
    // Get all servers
    const { servers } = await client.getServers();
    console.log('Available servers:', servers.map(s => s.name));

    // Execute a query
    const queryResult = await client.executeQuery(
      'airbnb',
      'Find hotels in Paris for 2 adults with a price less than 200 euros per night',
      'gpt-3.5-turbo'
    );
    console.log('Query result:', queryResult.result);

    // Add a new server
    await client.addServer('filesystem', 'npx', [
      '-y',
      '@modelcontextprotocol/server-filesystem',
      '/tmp'
    ]);
    console.log('Server added successfully');

    // Get tools for a server
    const { tools } = await client.getTools('playwright');
    console.log('Available tools:', tools.map(t => t.name));
  } catch (error) {
    console.error('Error:', error.message);
  }
}

main();
```

### Python Integration

#### Client Configuration
```python
import requests

class MCPCliClient:
    def __init__(self, base_url='http://localhost:8000/api'):
        self.base_url = base_url

    def request(self, endpoint, method='GET', data=None):
        url = f"{self.base_url}{endpoint}"
        
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        elif method == 'DELETE':
            response = requests.delete(url)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json()

    # Server management
    def get_servers(self):
        return self.request('/servers')

    def get_server(self, name):
        return self.request(f'/servers/{name}')

    def add_server(self, name, command, args=None, env=None):
        if args is None:
            args = []
        if env is None:
            env = {}
        return self.request('/servers', 'POST', {
            'name': name,
            'command': command,
            'args': args,
            'env': env
        })

    def remove_server(self, name):
        return self.request(f'/servers/{name}', 'DELETE')

    # Query execution
    def execute_query(self, server, query, model='gpt-3.5-turbo'):
        return self.request('/query', 'POST', {
            'server': server,
            'query': query,
            'model': model
        })

    # Tools management
    def get_tools(self, server_name, model='gpt-3.5-turbo'):
        return self.request(f'/servers/{server_name}/tools?model={model}')

    # Configuration management
    def export_config(self, filepath):
        return self.request('/config/export', 'POST', {'filepath': filepath})

    def import_config(self, filepath):
        return self.request('/config/import', 'POST', {'filepath': filepath})
```

#### Usage Example
```python
def main():
    client = MCPCliClient('http://localhost:8000/api')

    try:
        # Get all servers
        servers_response = client.get_servers()
        print('Available servers:', [s['name'] for s in servers_response['servers']])

        # Execute a query
        query_result = client.execute_query(
            'airbnb',
            'Find hotels in Paris for 2 adults with a price less than 200 euros per night',
            'gpt-3.5-turbo'
        )
        print('Query result:', query_result['result'])

        # Add a new server
        client.add_server('filesystem', 'npx', [
            '-y',
            '@modelcontextprotocol/server-filesystem',
            '/tmp'
        ])
        print('Server added successfully')

        # Get tools for a server
        tools_response = client.get_tools('playwright')
        print('Available tools:', [t['name'] for t in tools_response['tools']])
    except Exception as e:
        print('Error:', str(e))

if __name__ == '__main__':
    main()
```

## Errors and Status Codes

The API uses standard HTTP status codes to indicate the success or failure of a request:

| Code | Description |
|------|-------------|
| 200  | OK - The request was successfully completed |
| 400  | Bad Request - The request contains missing or invalid parameters |
| 404  | Not Found - The requested resource was not found |
| 500  | Internal Server Error - An error occurred while processing the request |

In case of an error, the response will contain a JSON object with the following format:

```json
{
  "error": "Detailed description of the error"
}
```

## Security Considerations

The current implementation of the API does not include authentication or authorization mechanisms. It is recommended to:

1. Run the server only on trusted networks or behind a reverse proxy with authentication
2. Use HTTPS to protect communications
3. Limit access to the API using firewalls or other access control mechanisms
4. Consider implementing authentication via JWT tokens or API keys for production environments

## Performance and Optimization

- The API server is designed to handle both synchronous and asynchronous requests
- Operations that require interactions with external MCP servers may take longer
- For high workloads, consider implementing a caching system for frequent query results
- For production deployments, use a WSGI server like Gunicorn or uWSGI instead of the Flask development server

## Troubleshooting

### Server doesn't start

- Verify that dependencies are correctly installed: `pip install -e .`
- Check that the specified port is not already in use (on macOS, port 5000 is often used by AirPlay)
- Make sure you have the necessary permissions for network access

### Errors during query execution

- Verify that the specified MCP server is correctly configured
- Make sure the OpenAI API key is set in the environment (`OPENAI_API_KEY` environment variable)
- Check that the MCP server is able to handle the specified type of query

## Compatibility

The API has been tested with:
- Python 3.8+
- Flask 3.1+
- JavaScript/Node.js (via fetch API)
- curl and other HTTP clients

## Support and Contributions

For issues, feature requests, or contributions, please visit the project's GitHub repository or contact the MCP development team.

---

This documentation is intended to facilitate the integration of the MCP CLI API into any external application. For more information about MCP servers and their usage, please refer to the Model Context Protocol project documentation. 