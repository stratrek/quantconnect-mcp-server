# mcp-server
Python MCP server for local interactions with the QuantConnect API

## Available Tools (34)
| Tools provided by this Server | Short Description |
| -------- | ------- |
| `read_account` | Read the organization account status. |
| `create_project` | Create a new project in your default organization. |
| `read_project` | List the details of a project. |
| `list_projects` | List the details of all projects. |
| `update_project` | Update a project's name or description. |
| `delete_project` | Delete a project. |
| `create_project_collaborator` | Add a collaborator to a project. |
| `read_project_collaborators` | List all collaborators on a project. |
| `update_project_collaborator` | Update collaborator information in a project. |
| `delete_project_collaborator` | Remove a collaborator from a project. |
| `read_project_nodes` | Read the available and selected nodes of a project. |
| `update_project_nodes` | Update the active state of the given nodes to true. |
| `create_compile` | Asynchronously create a compile job request for a project. |
| `read_compile` | Read a compile packet job result. |
| `create_file` | Add a file to a given project. |
| `read_file` | Read a file from a project, or all files in the project if no file name is provided. |
| `update_file_name` | Update the name of a file. |
| `update_file_contents` | Update the contents of a file. |
| `delete_file` | Delete a file in a project. |
| `create_backtest` | Create a new backtest request and get the backtest Id. |
| `read_backtest` | Read the results of a backtest. |
| `list_backtests` | List all the backtests for the project. |
| `read_backtest_chart` | Read a chart from a backtest. |
| `read_backtest_orders` | Read out the orders of a backtest. |
| `read_backtest_insights` | Read out the insights of a backtest. |
| `update_backtest` | Update the name or note of a backtest. |
| `delete_backtest` | Delete a backtest from a project. |
| `estimate_optimization_cost` | Estimate the execution time of an optimization with the specified parameters. |
| `create_optimization` | Create an optimization with the specified parameters. |
| `read_optimization` | Read an optimization. |
| `list_optimizations` | List all the optimizations for a project. |
| `update_optimization` | Update the name of an optimization. |
| `abort_optimization` | Abort an optimization. |
| `delete_optimization` | Delete an optimization. |


## Configuration Examples
To connect local MCP clients (like Claude Desktop) to the QC MCP Server, follow these steps:

1. Install Docker Desktop and Claude Desktop.
2. Clone this repository to your local machine.
3. In a terminal, navigate to the project and then run `docker build -t mcp-server .`.
4. Add the following JSON to your configuration file:
```json
{
  "mcpServers": {
    "quantconnect": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "QUANTCONNECT_USER_ID",
        "-e", "QUANTCONNECT_API_TOKEN",
        "--name",
        "quantconnect-mcp-server",
        "mcp-server"
      ],
      "env": {
        "QUANTCONNECT_USER_ID": "<your_user_id>",
        "QUANTCONNECT_API_TOKEN": "<your_api_token"
      }
    }
  }
}
```
5. Open Claude Desktop.

## Debugging

### Logs
 To log to the `mcp-server-quantconnect.log` file, `import sys` and then `print("Hello world", file=sys.stderr)`.

### Inspector
 To start the inspector, run `npx @modelcontextprotocol/inspector uv run src/main.py`.
 To pass a model to the inspector tool, use JSON (for example, `{"name":"My Project","language":"Py"}`).
