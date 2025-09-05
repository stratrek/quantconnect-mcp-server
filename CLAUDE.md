# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **official QuantConnect MCP Server** - a Python-based Model Context Protocol server that enables AI assistants (like Claude) to interact with the QuantConnect platform API. It provides 64+ tools for project management, backtesting, live trading, optimization, and algorithm development.

## Development Commands

### Core Development
- **Run server locally**: `uv run src/main.py`
- **Run tests**: `pytest` (uses pythonpath configuration from pyproject.toml)
- **Run single test**: `pytest tests/test_filename.py::test_function_name`
- **Install dependencies**: `uv sync`
- **Add new dependency**: `uv add package_name`

### Docker Operations
- **Build image**: `docker build -t quantconnect/mcp-server .`
- **Run with stdio**: `docker run -i --rm -e QUANTCONNECT_USER_ID -e QUANTCONNECT_API_TOKEN quantconnect/mcp-server`
- **Run with HTTP**: Set `MCP_TRANSPORT=http`, `MCP_HOST`, `MCP_PORT` environment variables

### Testing
- **Inspector**: `npx @modelcontextprotocol/inspector uv run src/main.py`
- **HTTP testing**: Available test files: `test_http_client.py`, `test_mcp_http_client.py`

## Architecture

### Core Structure
- **`src/main.py`**: Entry point that registers all tools with FastMCP server
- **`src/tools/`**: Modular tool implementations (account, project, backtests, live trading, etc.)
- **`src/api_connection.py`**: HTTP client for QuantConnect API
- **`src/organization_workspace.py`**: Local workspace management
- **`src/models.py`**: Shared data models
- **`tests/`**: Comprehensive test suite with algorithm examples

### Tool Categories
1. **Account & Project Management**: `account.py`, `project.py`, `project_collaboration.py`, `project_nodes.py`
2. **Development**: `files.py`, `compile.py`, `ai.py` (PEP8, syntax checking, code completion)
3. **Testing**: `backtests.py`, `optimizations.py`
4. **Trading**: `live.py`, `live_commands.py`
5. **Infrastructure**: `object_store.py`, `lean_versions.py`, `mcp_server_version.py`

### Key Design Patterns
- Each tool category has its own module with registration function
- All tools use shared `api_connection.py` for API calls
- Error handling and logging throughout
- Support for both stdio (Claude Desktop) and HTTP transports

## Important Conventions

### QuantConnect-Specific Rules
- Never overwrite indicator method names (e.g., don't assign to `self.rsi`, use `self._rsi` instead)
- Always choose variable names different from methods being called
- Use PEP8 style for Python code (snake_case)
- Compile code before running backtests using `create_compile` and `read_compile`
- Use `patch_file` tool for line-specific updates instead of `update_file_contents` when more efficient

### Authentication
- Requires `QUANTCONNECT_USER_ID` and `QUANTCONNECT_API_TOKEN` environment variables
- Optional `AGENT_NAME` for tracking request sources

### Transport Modes
- **stdio**: Default for MCP clients like Claude Desktop
- **http/streamable-http**: For HTTP-based integrations, uses `MCP_HOST` and `MCP_PORT`

## Testing Strategy

The repository includes extensive test coverage with real algorithm examples in `tests/algorithms/` for various scenarios (parameter optimization, live trading, error handling, etc.). Tests are organized by functionality and include both unit tests and integration tests.