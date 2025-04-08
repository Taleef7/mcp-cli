# MCP CLI API Technical Documentation

This document provides technical details about the implementation of the MCP CLI API server (`server.py`). It covers the architecture, design patterns, and internal workings of the API module.

## Architecture Overview

The MCP CLI API server is built using Flask, a lightweight WSGI web application framework. The server exposes RESTful endpoints that map to core MCP CLI functionality, allowing clients to interact with MCP servers via HTTP requests.

### Key Components

1. **Flask Application**: The main web application that handles HTTP requests
2. **CORS Support**: Cross-Origin Resource Sharing enabled for frontend integration
3. **Async Handling**: Custom integration of asyncio with Flask for async operations
4. **JSON API**: Consistent JSON-based request and response formats
5. **Error Handling**: Standardized error responses with appropriate HTTP status codes

## Module Structure

The `server.py` module is organized as follows:

```
server.py
├── Imports and setup
├── Helper functions (run_async)
├── Status endpoint
├── Servers endpoints
│   ├── GET /api/servers
│   ├── GET /api/servers/<name>
│   ├── POST /api/servers
│   ├── PUT /api/servers/<name>
│   └── DELETE /api/servers/<name>
├── Query endpoint
│   └── POST /api/query
├── Tools endpoint
│   └── GET /api/servers/<name>/tools
├── Configuration endpoints
│   ├── POST /api/config/export
│   └── POST /api/config/import
├── Command-line argument parsing
└── Main entry point
```

## Core Functionality

### Asynchronous Operations

The MCP CLI core functions are asynchronous, but Flask routes are synchronous. To bridge this gap, the API server uses a helper function `run_async` that creates a new event loop for each async operation:

```python
def run_async(coroutine):
    """Run an async function in a Flask route."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coroutine)
    finally:
        loop.close()
```

This function is used whenever an endpoint needs to call an async function from the MCP CLI core, such as running queries or listing tools.

### Request/Response Handling

All endpoints follow a consistent pattern:

1. Validate the request (body parameters, URL parameters, etc.)
2. Call the appropriate core function
3. Return a JSON response with appropriate status codes

Success responses include a `status` field with value `"success"` and optionally a `message` field with a human-readable message. Error responses include an `error` field with a description of the error.

### Tool Parsing

The `/api/servers/<name>/tools` endpoint includes special logic for parsing the text output from MCP CLI's `list_tools` function into a structured JSON format. This involves:

1. Parsing each tool's name, description, and parameters
2. Handling potential JSON parsing errors for parameters
3. Constructing a clean JSON response with properly formatted tool definitions

```python
# Parse the text result into a structured format
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
            # Complex JSON parsing logic...
            current_tool['parameters'] = json.loads(params_text)
        except json.JSONDecodeError:
            current_tool['parameters'] = {"error": "Failed to parse parameters"}
```

## Error Handling Strategy

The API server implements a consistent error handling strategy:

1. **Validation Errors**: Return 400 Bad Request with a descriptive error message
2. **Resource Not Found**: Return 404 Not Found with information about available resources
3. **Server Errors**: Return 500 Internal Server Error with a description of what went wrong

All errors are caught and handled to prevent the server from crashing and to provide helpful information to clients.

## Configuration Management

The API server interacts with the MCP CLI configuration file using the core functions `load_config`, `save_config`, `export_config`, and `import_config`. These functions handle:

1. Reading the configuration from disk
2. Validating changes to the configuration
3. Writing updated configuration back to disk
4. Exporting/importing configuration to/from files

## Command Line Interface

The server includes a command-line interface with the following options:

```python
def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="MCP CLI API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the server on")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    return parser.parse_args()
```

These options allow users to customize the host, port, and debug settings when starting the server.

## Security Considerations

The current implementation does not include authentication or authorization mechanisms. When deploying in a production environment, consider:

1. Adding authentication (e.g., API keys, OAuth)
2. Implementing TLS/SSL
3. Setting up proper CORS restrictions
4. Adding rate limiting to prevent abuse

## Logging

The API server uses Python's standard logging module for logging information and errors:

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

Logs include timestamps, module names, log levels, and messages, which can be useful for debugging and monitoring.

## Extending the API

To add a new endpoint to the API:

1. Define a new Flask route with the appropriate HTTP method
2. Implement request validation
3. Call the necessary MCP CLI core function(s)
4. Return a JSON response following the established patterns

Example:

```python
@app.route('/api/new_endpoint', methods=['POST'])
def new_endpoint():
    """Description of the new endpoint."""
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Validate parameters
    if 'required_param' not in data:
        return jsonify({'error': 'required_param is required'}), 400
    
    try:
        # Call core function
        result = some_core_function(data['required_param'])
        
        # Return success response
        return jsonify({
            'status': 'success',
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

## Performance Considerations

- Each asynchronous operation creates a new event loop, which has some overhead
- For high-traffic deployments, consider using an ASGI server like Uvicorn with an async framework like FastAPI
- The current implementation does not include caching, which could improve performance for frequently accessed data

## Future Improvements

Potential improvements to consider:

1. **Authentication**: Add API key or OAuth-based authentication
2. **Pagination**: Implement pagination for endpoints that return lists
3. **Websockets**: Add websocket support for streaming query results
4. **Metrics**: Add endpoint for monitoring and metrics
5. **Swagger/OpenAPI**: Generate OpenAPI documentation
6. **Async Framework**: Consider migrating to an async-native framework like FastAPI
7. **Environment Variables**: Support configuration via environment variables
8. **Dockerization**: Provide a Dockerfile for containerized deployment

## Troubleshooting Common Issues

### Connection Refused

If clients cannot connect to the API server, check:
- The server is running
- The host and port are correctly configured
- Firewall settings allow connections to the specified port

### Timeout Errors

If requests time out, consider:
- Increasing the timeout for long-running operations
- Implementing background tasks for expensive operations
- Checking if MCP servers are responding in a timely manner

### JSON Parsing Errors

If clients report JSON parsing errors:
- Check that all responses are valid JSON
- Ensure that tools with complex parameters are properly parsed
- Validate that error responses maintain the expected format 