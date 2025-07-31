# mcp-server
Python MCP server for local interactions with the QuantConnect API

## Available Tools (60)
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
| `estimate_optimization_time` | Estimate the execution time of an optimization with the specified parameters. |
| `create_optimization` | Create an optimization with the specified parameters. |
| `read_optimization` | Read an optimization. |
| `list_optimizations` | List all the optimizations for a project. |
| `update_optimization` | Update the name of an optimization. |
| `abort_optimization` | Abort an optimization. |
| `delete_optimization` | Delete an optimization. |
| `authorize_connection` | Authorize an external connection with a live brokerage or data provider. |
| `create_live_algorithm` | Create a live algorithm. |
| `read_live_algorithm` | Read details of a live algorithm. |
| `list_live_algorithms` | List all your past and current live trading deployments. |
| `read_live_chart` | Read a chart from a live algorithm. |
| `read_live_logs` | Get the logs of a live algorithm. |
| `read_live_portfolio` | Read out the portfolio state of a live algorithm. |
| `read_live_orders` | Read out the orders of a live algorithm. |
| `read_live_insights` | Read out the insights of a live algorithm. |
| `stop_live_algorithm` | Stop a live algorithm. |
| `liquidate_live_algorithm` | Liquidate and stop a live algorithm. |
| `create_live_command` | Send a command to a live trading algorithm. |
| `broadcast_live_command` | Broadcast a live command to all live algorithms in an organization. |
| `upload_object` | Upload files to the Object Store. |
| `read_object_properties` | Get Object Store properties of a specific organization and key. |
| `read_object_store_file_job_id` | Create a job to download files from the Object Store and then read the job Id. |
| `read_object_store_file_download_url` | Get the URL for downloading files from the Object Store. |
| `list_object_store_files` | List the Object Store files under a specific directory in an organization. |
| `delete_object` | Delete the Object Store file of a specific organization and key. |
| `read_lean_versions` | Returns a list of LEAN versions with basic information for each version. |
| `check_initialization_errors` | Run a backtest for a few seconds to initialize the algorithm and get initialization errors if any. |
| `complete_code` | Show the code completion for a specific text input. |
| `enhance_error_message` | Show additional context and suggestions for error messages. |
| `update_code_to_pep8` | Update Python code to follow PEP8 style. |
| `check_syntax` | Check the syntax of a code. |
| `search_quantconnect` | Search for content in QuantConnect. |

## Getting Started
To connect local MCP clients (like Claude Desktop) to the QC MCP Server, follow these steps:

1. Install and open [Docker Desktop](https://docs.docker.com/desktop/).
2. In a terminal, pull the MCP Server from Docker Hub.
```
docker pull quantconnect/mcp-server
```
3. Install and open [Claude Desktop](https://claude.ai/download).
4. In Claude Desktop, click **File > Settings > Developer > Edit Config**.
5. Edit the `claude_desktop_config.json` file to include the following `quantconnect` configuration:
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
        "quantconnect/mcp-server"
      ],
      "env": {
        "QUANTCONNECT_USER_ID": "<your_user_id>",
        "QUANTCONNECT_API_TOKEN": "<your_api_token"
      }
    }
  }
}
```
  To get your user Id and API token, see [Request API Token](https://www.quantconnect.com/docs/v2/cloud-platform/community/profile#09-Request-API-Token).

6. Restart Claude Desktop.

To view all the MCP clients and the features they support, see the [Feature Support Matrix](https://modelcontextprotocol.io/clients#feature-support-matrix) in the MCP documentation.

## Debugging

### Logs
 To log to the `mcp-server-quantconnect.log` file, `import sys` and then `print("Hello world", file=sys.stderr)`.

### Inspector
 To start the inspector, run `npx @modelcontextprotocol/inspector uv run src/main.py`.
 To pass a model to the inspector tool, use JSON (for example, `{"name":"My Project","language":"Py"}`).
