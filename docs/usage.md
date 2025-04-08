# Using MCP CLI, GUI & API

This guide covers how to use all components of the MCP CLI & GUI project: the command-line interface, the graphical user interface, and the API server.

## Command-Line Interface (CLI)

The command-line interface provides commands for managing MCP servers and interacting with them through OpenAI models.

### Available Commands

#### List Configured Servers

```bash
mcp list
```

#### Add a New MCP Server

```bash
mcp add <name> <command> <arguments...> [--env KEY=VALUE...]
```

Examples:

```bash
# Add a Playwright server for web browsing
mcp add playwright npx @playwright/mcp@latest --env DISPLAY=:1

# Add an Airbnb server for accommodation search
mcp add airbnb npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt

# Add a Filesystem server for local file access
mcp add filesystem npx -y @modelcontextprotocol/server-filesystem /path/to/directory
```

#### Remove an MCP Server

```bash
mcp remove <name>
```

#### View Detailed Information about a Server

```bash
mcp info <server>
```

#### List Tools Available from a Server

```bash
mcp tools <server> [--model <model>]
```

Example:

```bash
mcp tools playwright --model gpt-4
```

#### Run a Query on an MCP Server

```bash
mcp run <server> "<query>" [--model <model>]
```

Examples:

```bash
# Web search with Playwright
mcp run playwright "Find the best restaurants in San Francisco"

# Search for accommodations on Airbnb
mcp run airbnb "Find a nice place to stay in Barcelona for 2 adults for a weekend in July"

# Work with local files
mcp run filesystem "List all Python files and summarize their content"
```

#### Export Configuration

```bash
mcp export <filepath>
```

#### Import Configuration

```bash
mcp import <filepath>
```

## Graphical User Interface (GUI)

The GUI provides a more user-friendly way to interact with MCP servers.

### Starting the GUI

```bash
# Using the installed package
mcp-gui

# Using the Python module
python -m mcp_cli

# Using the script directly
python bin/mcp_gui.py
```

### GUI Features

- **Server Management**: Add, remove, and view details of MCP servers
- **Query Execution**: Run queries against servers and view results
- **Tool Explorer**: Browse available tools from each server
- **Query History**: View and reuse previous queries
- **Configuration Management**: Import and export configurations

## API Server

The API server provides a RESTful interface to MCP CLI functionality, allowing integration with web applications and other services.

### Starting the API Server

```bash
# Using the installed package
mcp-server

# With custom host and port
mcp-server --host 127.0.0.1 --port 8080

# In debug mode
mcp-server --debug
```

### API Endpoints

- `GET /api/status`: Health check endpoint
- `GET /api/servers`: List all configured MCP servers
- `GET /api/servers/{name}`: Get information about a specific server
- `POST /api/servers`: Add a new server
- `PUT /api/servers/{name}`: Update an existing server
- `DELETE /api/servers/{name}`: Remove a server
- `POST /api/query`: Run a query against an MCP server
- `GET /api/servers/{name}/tools`: List tools provided by a server
- `POST /api/config/export`: Export configuration to a file
- `POST /api/config/import`: Import configuration from a file

For detailed API documentation, refer to:
- [API Reference](../mcp_cli/api/README.md)
- [API Quickstart Guide](../mcp_cli/api/QUICKSTART.md)

## Common Use Cases

### Web Research with Playwright

```bash
# Add the Playwright server
mcp add playwright npx @playwright/mcp@latest --env DISPLAY=:1

# Run a web search query
mcp run playwright "Research the impact of artificial intelligence on healthcare"
```

### Travel Planning with Airbnb

```bash
# Add the Airbnb server
mcp add airbnb npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt

# Search for accommodations
mcp run airbnb "Find a beachfront apartment in Miami for a family of 4 for the first week of June"
```

### Local File Management

```bash
# Add the Filesystem server
mcp add filesystem npx -y @modelcontextprotocol/server-filesystem /path/to/directory

# Work with local files
mcp run filesystem "Find all JavaScript files older than 6 months and summarize their content"
```

## Configuration

MCP CLI stores its configuration in `config/config.json` in the project directory (or in the installation directory if installed via pip). This file contains all your MCP server configurations and can be exported or imported.

## Troubleshooting

- **Error connecting to server**: Make sure the MCP server is installed and available. For NPM-based servers, try installing them globally first.
- **API key errors**: Ensure your OpenAI API key is set correctly in the `.env` file or as an environment variable.
- **Tool not found**: Some tools might require specific server configurations or additional setup. Check the server documentation.
- **GUI not starting**: Make sure PyQt5 is installed correctly: `pip install PyQt5`.
- **API server errors**: Check logs for details. Ensure port is not in use by another application.

## Advanced Usage

### Using a Different OpenAI Model

You can specify a different OpenAI model for queries:

```bash
mcp run playwright "Find recent news about space exploration" --model gpt-4
```

### Environment Variables

You can set environment variables for MCP servers:

```bash
mcp add playwright npx @playwright/mcp@latest --env DISPLAY=:1 DEBUG=pw:api
```

### Running Queries Programmatically

You can use the MCP CLI as a Python library in your own scripts:

```python
from mcp_cli.core import run_query
import asyncio

async def main():
    result = await run_query("playwright", "Find information about climate change", "gpt-3.5-turbo", True)
    print(result)

asyncio.run(main())
``` 