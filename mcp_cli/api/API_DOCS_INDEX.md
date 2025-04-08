# MCP CLI API Documentation

Welcome to the comprehensive documentation for the MCP CLI API. This API allows you to interact with Model Context Protocol (MCP) servers via HTTP requests, providing a powerful interface for managing servers, running queries, and discovering tools.

## Documentation Index

This API documentation consists of several specialized documents, each addressing a specific aspect of the API:

1. **[API Reference](README.md)** - Complete endpoint reference with request/response formats
2. **[Technical Documentation](TECHNICAL_DOCS.md)** - Detailed implementation and architecture overview
3. **[Quickstart Guide](QUICKSTART.md)** - Get up and running quickly with common use cases
4. **[Postman Collection](MCP_CLI_API.postman_collection.json)** - Ready-to-use Postman collection for testing

## Overview

The MCP CLI API server exposes a RESTful interface for interacting with Model Context Protocol (MCP) servers. It provides endpoints for:

- Managing server configurations (add, update, remove)
- Running queries against MCP servers
- Discovering tools provided by MCP servers
- Exporting and importing configurations

The API is designed to be simple, consistent, and easy to integrate with any client application.

## Key Features

- **RESTful API**: Clean, resource-oriented design following REST principles
- **JSON-based**: Consistent JSON request/response formats
- **Error Handling**: Standardized error responses with appropriate HTTP status codes
- **Async Operations**: Handles asynchronous operations for running queries
- **Tools Discovery**: Ability to dynamically discover tools provided by MCP servers

## Getting Started

For a quick introduction, visit the [Quickstart Guide](QUICKSTART.md), which walks you through:

- Installing the necessary components
- Starting the API server
- Basic usage examples
- Troubleshooting common issues

## API Reference

The [API Reference](README.md) provides detailed documentation for each endpoint, including:

- Endpoint URLs and methods
- Request parameters and body format
- Response format and status codes
- Example requests and responses

## Technical Details

The [Technical Documentation](TECHNICAL_DOCS.md) dives into the implementation details, covering:

- Architecture overview
- Core functionality
- Error handling strategy
- Configuration management
- Security considerations
- Extending the API

## Testing with Postman

The [Postman Collection](MCP_CLI_API.postman_collection.json) allows you to quickly test the API endpoints:

1. Import the collection into Postman
2. Set the `baseUrl` variable (default: `http://localhost:5000`)
3. Start making requests to explore the API

## Further Resources

- [MCP CLI Project Repository](https://github.com/your-org/mcp-cli-project)
- [Model Context Protocol Documentation](https://github.com/modelcontextprotocol/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)

## Contributing

We welcome contributions to improve the API and its documentation. Please refer to the project repository for contribution guidelines.

## License

This API and its documentation are released under the MIT License.

---

**Note:** The MCP CLI API is built to integrate with any MCP-compatible server, allowing for a standardized way to interact with various tools and services through language models. 