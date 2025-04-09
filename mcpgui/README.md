# MCP CLI GUI

A simple web interface to interact with the MCP CLI API, implemented in Next.js.

## Features

- MCP server management (add, remove, view)
- Running queries on MCP servers
- Viewing available tools on each server
- Configuration import/export
- Modern and responsive interface

## Prerequisites

- Node.js 18 or higher
- A running MCP CLI API server

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-cli-gui.git
cd mcp-cli-gui

# Install dependencies
npm install

# Start the development server
npm run dev
```

## Configuration

By default, the application connects to an MCP CLI API server at `http://localhost:8000/api`. To change this URL, you can modify the `src/lib/api-client.ts` file.

```typescript
// Change this value to point to your MCP CLI API server
const baseUrl = 'http://localhost:8000/api';
```

## Usage

### Server Management

In the "Servers" section, you can:
- View the list of configured MCP servers
- Add new servers specifying name, command, arguments, and environment variables
- Remove existing servers

### Query Execution

In the "Query" section, you can:
- Select an MCP server from the configured ones
- Specify the model to use (default: gpt-3.5-turbo)
- Enter a query to execute
- View the execution result

### Tools Viewing

In the "Tools" section, you can:
- Select an MCP server
- View the list of available tools on that server
- Expand each tool to see the description and required parameters

### Configuration Management

In the "Configuration" section, you can:
- Import an existing configuration from a file
- Export the current configuration to a file

## Development

### Project Structure

```
src/
├── app/                 # Next.js pages (app router)
├── components/          # React components
│   ├── ui/              # Reusable UI components
│   └── ...              # Application-specific components
├── lib/                 # Libraries and utilities
└── ...
```

### Commands

```bash
# Start the development server
npm run dev

# Build the application for production
npm run build

# Start the application in production mode
npm start

# Run linting
npm run lint
```

## License

MIT
