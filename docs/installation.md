# Installing MCP CLI & GUI

This guide will help you install MCP CLI & GUI, a toolkit for interacting with Model Context Protocol (MCP) servers using OpenAI models.

## Prerequisites

- Python 3.8+
- pip
- PyQt5 (for the GUI component)
- An OpenAI API key

## Installation Methods

### Installing from Source

1. Clone the repository or download the archive:

```bash
git clone https://github.com/your-org/mcp-cli-project.git
cd mcp-cli-project
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

3. Install the package in development mode:

```bash
pip install -e .
```

### Installing with pip

```bash
pip install mcp-cli
```

## Configuration

1. Set your OpenAI API key in a `.env` file in your working directory or as an environment variable:

```bash
# In .env file
OPENAI_API_KEY=your_openai_api_key
```

or

```bash
# From command line
export OPENAI_API_KEY=your_openai_api_key  # on Windows: set OPENAI_API_KEY=your_openai_api_key
```

2. Add an MCP server:

```bash
# Using the command-line tool
mcp add <server_name> <command> <arguments...> [--env KEY=VALUE...]

# Or using the Python module
python -m mcp_cli add <server_name> <command> <arguments...> [--env KEY=VALUE...]
```

Example:

```bash
# Add the Playwright server for web browsing
mcp add playwright npx @playwright/mcp@latest --env DISPLAY=:1

# Add the Airbnb server for accommodation search
mcp add airbnb npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt
```

## Verifying Installation

You can verify your installation by running:

```bash
# Check the CLI
mcp list

# Start the GUI
mcp-gui

# Start the API server
mcp-server
```

## Development Installation

If you plan to contribute to the project, install the development dependencies:

```bash
pip install -e ".[dev]"
```

And set up pre-commit hooks:

```bash
pre-commit install
```

## Troubleshooting Installation

### Common Issues

- **PyQt5 installation errors**: Try installing it separately with `pip install PyQt5`
- **OpenAI API key not found**: Ensure your `.env` file is in the correct directory or set the environment variable
- **Command not found**: Make sure the package is properly installed and your PATH is set correctly
- **MCP server not installing**: For NPM-based servers, ensure Node.js and NPM are installed

### Environment-Specific Issues

#### Windows
- Ensure you have the Microsoft C++ Build Tools installed for some dependencies
- Use `set` instead of `export` for environment variables

#### macOS
- You may need to install Xcode Command Line Tools for some dependencies

#### Linux
- Ensure you have the required development libraries for Qt (for the GUI component)

## Next Steps

After installation, please refer to the [usage guide](usage.md) for instructions on how to use MCP CLI & GUI. 