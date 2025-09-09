<img width="1575" height="280" alt="github-header" src="https://github.com/user-attachments/assets/6cec1ef7-0340-416e-ab81-c73fbc8ff847" />

# QuantConnect MCP Server

The QuantConnect MCP Server is a bridge for AIs (such as Claude and OpenAI o3 Pro) to interact with our cloud platform. When equipped with our MCP, the AI can perform tasks on your behalf through our API such as updating projects, writing strategies, backtesting, and deploying strategies to production live-trading.

This is the OFFICIAL implementation of QuantConnect's MCP, maintained by the QuantConnect team. We recommend using the official version to ensure security of your code and API tokens. Our implementation is tested and dockerized for easy cross-platform deployment.

## Getting Started

To connect local MCP clients (like Claude Desktop) to the QC MCP Server, follow these steps:

1. Install and open [Docker Desktop](https://docs.docker.com/desktop/).
2. Install and open [Claude Desktop](https://claude.ai/download).
3. In Claude Desktop, click **File > Settings > Developer > Edit Config**.
4. Edit the `claude_desktop_config.json` file to include the following `quantconnect` configuration:

```json
{
  "mcpServers": {
    "quantconnect": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "QUANTCONNECT_USER_ID",
        "-e",
        "QUANTCONNECT_API_TOKEN",
        "-e",
        "AGENT_NAME",
        "--platform",
        "<your_platform>",
        "quantconnect/mcp-server"
      ],
      "env": {
        "QUANTCONNECT_USER_ID": "<your_user_id>",
        "QUANTCONNECT_API_TOKEN": "<your_api_token>",
        "AGENT_NAME": "MCP Server"
      }
    }
  }
}
```

To get your user Id and API token, see [Request API Token](https://www.quantconnect.com/docs/v2/cloud-platform/community/profile#09-Request-API-Token).

Our MCP server is multi-platform capable. The options are `linux/amd64` for Intel/AMD chips and `linux/arm64` for ARM chips (for example, Apple's M-series chips).

If you simultaneously run multiple agents, set a unique value for the `AGENT_NAME` environment variable for each agent to keep record of the request source.

5. Restart Claude Desktop.

   Claude Desktop automatically pulls our MCP server from Docker Hub and connects to it.

To view all the MCP clients and the features they support, see the [Feature Support Matrix](https://modelcontextprotocol.io/clients#feature-support-matrix) in the MCP documentation.

To keep the Docker image up-to-date, pull the latest MCP server from Docker Hub in the terminal.

```
docker pull quantconnect/mcp-server
```

If you have an ARM chip, add the `--platform linux/arm64` option.

## ⚡ NEW: Token-Optimized Brief Tools

For improved LLM performance and reduced token usage, we've added lightweight "brief" versions of key backtest tools:

| Tool | Purpose | Benefits |
|------|---------|----------|
| `create_backtest_brief` | Create backtests with minimal response data | Returns only `backtestId` and `status` instead of full backtest object |
| `read_backtest_brief` | Check backtest status efficiently | Returns only `status`, `error`, and `hasInitializeError` fields |
| `read_backtest_statistics` | Get key performance metrics from backtests | Returns ~20 essential statistics instead of 100+ fields |
| `wait_for_backtest` | Poll for backtest completion | Efficiently waits for completion with configurable timeout and polling interval |

These tools are designed to reduce API response size by 90%+ compared to their full counterparts, making them ideal for AI assistants and automated workflows.

## Available Tools (68)

| Tools provided by this Server         | Short Description                                                                                |
| ------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `read_account`                        | Read the organization account status.                                                            |
| `create_project`                      | Create a new project in your default organization.                                               |
| `read_project`                        | List the details of a project or a set of recent projects.                                       |
| `list_projects`                       | List the details of all projects.                                                                |
| `update_project`                      | Update a project's name or description.                                                          |
| `delete_project`                      | Delete a project.                                                                                |
| `create_project_collaborator`         | Add a collaborator to a project.                                                                 |
| `read_project_collaborators`          | List all collaborators on a project.                                                             |
| `update_project_collaborator`         | Update collaborator information in a project.                                                    |
| `delete_project_collaborator`         | Remove a collaborator from a project.                                                            |
| `lock_project_with_collaborators`     | Lock a project so you can edit it.                                                               |
| `read_project_nodes`                  | Read the available and selected nodes of a project.                                              |
| `update_project_nodes`                | Update the active state of the given nodes to true.                                              |
| `create_compile`                      | Asynchronously create a compile job request for a project.                                       |
| `read_compile`                        | Read a compile packet job result.                                                                |
| `create_file`                         | Add a file to a given project.                                                                   |
| `read_file`                           | Read a file from a project, or all files in the project if no file name is provided.             |
| `update_file_name`                    | Update the name of a file.                                                                       |
| `update_file_contents`                | Update the contents of a file.                                                                   |
| `patch_file`                          | Apply a patch (unified diff) to a file in a project.                                             |
| `delete_file`                         | Delete a file in a project.                                                                      |
| `create_backtest`                     | Create a new backtest request and get the backtest Id.                                           |
| `create_backtest_brief` ⚡            | **NEW**: Create a backtest with minimal response data to reduce token usage.                     |
| `read_backtest`                       | Read the results of a backtest.                                                                  |
| `read_backtest_brief` ⚡            | **NEW**: Get brief backtest status (status, error, hasInitializeError only).                    |
| `read_backtest_statistics` ⚡         | **NEW**: Get key performance statistics from backtest results.                                  |
| `wait_for_backtest` ⚡                | **NEW**: Poll for backtest completion with configurable timeout and interval.                   |
| `list_backtests`                      | List all the backtests for the project.                                                          |
| `read_backtest_chart`                 | Read a chart from a backtest.                                                                    |
| `read_backtest_orders`                | Read out the orders of a backtest.                                                               |
| `read_backtest_insights`              | Read out the insights of a backtest.                                                             |
| `update_backtest`                     | Update the name or note of a backtest.                                                           |
| `delete_backtest`                     | Delete a backtest from a project.                                                                |
| `estimate_optimization_time`          | Estimate the execution time of an optimization with the specified parameters.                    |
| `create_optimization`                 | Create an optimization with the specified parameters.                                            |
| `read_optimization`                   | Read an optimization.                                                                            |
| `list_optimizations`                  | List all the optimizations for a project.                                                        |
| `update_optimization`                 | Update the name of an optimization.                                                              |
| `abort_optimization`                  | Abort an optimization.                                                                           |
| `delete_optimization`                 | Delete an optimization.                                                                          |
| `authorize_connection`                | Authorize an external connection with a live brokerage or data provider.                         |
| `create_live_algorithm`               | Create a live algorithm.                                                                         |
| `read_live_algorithm`                 | Read details of a live algorithm.                                                                |
| `list_live_algorithms`                | List all your past and current live trading deployments.                                         |
| `read_live_chart`                     | Read a chart from a live algorithm.                                                              |
| `read_live_logs`                      | Get the logs of a live algorithm.                                                                |
| `read_live_portfolio`                 | Read out the portfolio state of a live algorithm.                                                |
| `read_live_orders`                    | Read out the orders of a live algorithm.                                                         |
| `read_live_insights`                  | Read out the insights of a live algorithm.                                                       |
| `stop_live_algorithm`                 | Stop a live algorithm.                                                                           |
| `liquidate_live_algorithm`            | Liquidate and stop a live algorithm.                                                             |
| `create_live_command`                 | Send a command to a live trading algorithm.                                                      |
| `broadcast_live_command`              | Broadcast a live command to all live algorithms in an organization.                              |
| `upload_object`                       | Upload files to the Object Store.                                                                |
| `read_object_properties`              | Get Object Store properties of a specific organization and key.                                  |
| `read_object_store_file_job_id`       | Create a job to download files from the Object Store and then read the job Id.                   |
| `read_object_store_file_download_url` | Get the URL for downloading files from the Object Store.                                         |
| `list_object_store_files`             | List the Object Store files under a specific directory in an organization.                       |
| `delete_object`                       | Delete the Object Store file of a specific organization and key.                                 |
| `read_lean_versions`                  | Returns a list of LEAN versions with basic information for each version.                         |
| `check_initialization_errors`         | Run a backtest for a few seconds to initialize the algorithm and get inialization errors if any. |
| `complete_code`                       | Show the code completion for a specific text input.                                              |
| `enhance_error_message`               | Show additional context and suggestions for error messages.                                      |
| `update_code_to_pep8`                 | Update Python code to follow PEP8 style.                                                         |
| `check_syntax`                        | Check the syntax of a code.                                                                      |
| `search_quantconnect`                 | Search for content in QuantConnect.                                                              |
| `read_mcp_server_version`             | Returns the version of the QC MCP Server that's running.                                         |
| `read_latest_mcp_server_version`      | Returns the latest version of the QC MCP Server released.                                        |

---

## Tool Details

**Tool:** `read_account`

Read the organization account status.

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `create_project`

Create a new project in your default organization.

| Parameter        | Type                | Description                                                                                                         |
| ---------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `name`           | `string`            | Project name.                                                                                                       |
| `language`       | `string`            | Programming language to use.                                                                                        |
| `organizationId` | `string` _optional_ | The organization to create project under. If you don't provide a value, it defaults to your preferred organization. |

_This tool modifies it's environment._

_This tool doesn't perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_project`

List the details of a project or a set of recent projects.

| Parameter   | Type                 | Description                                                                                                                  |
| ----------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `projectId` | `integer` _optional_ | Id of the project to read.                                                                                                   |
| `start`     | `integer` _optional_ | Starting (inclusive, zero-based) index of the projects to fetch. If you provide this property, omit the project Id property. |
| `end`       | `integer` _optional_ | Last (exlusive) index of the projects to fetch. If you provide this property, omit the project Id property.                  |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `list_projects`

List the details of all projects.

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `update_project`

Update a project's name or description.

| Parameter     | Type                | Description                           |
| ------------- | ------------------- | ------------------------------------- |
| `projectId`   | `integer`           | Project Id to which the file belongs. |
| `name`        | `string` _optional_ | The new name for the project.         |
| `description` | `string` _optional_ | The new description for the project.  |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `delete_project`

Delete a project.

| Parameter   | Type      | Description                  |
| ----------- | --------- | ---------------------------- |
| `projectId` | `integer` | Id of the project to delete. |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `create_project_collaborator`

Add a collaborator to a project.

| Parameter                  | Type      | Description                                         |
| -------------------------- | --------- | --------------------------------------------------- |
| `projectId`                | `integer` | Id of the project to add the collaborator to.       |
| `collaboratorUserId`       | `string`  | User Id of the collaborator to add.                 |
| `collaborationLiveControl` | `boolean` | Gives the right to deploy and stop live algorithms. |
| `collaborationWrite`       | `boolean` | Gives the right to edit the code.                   |

_This tool modifies it's environment._

_This tool doesn't perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_project_collaborators`

List all collaborators on a project.

| Parameter   | Type      | Description                                             |
| ----------- | --------- | ------------------------------------------------------- |
| `projectId` | `integer` | Id of the project from which to read the collaborators. |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `update_project_collaborator`

Update collaborator information in a project.

| Parameter            | Type      | Description                                         |
| -------------------- | --------- | --------------------------------------------------- |
| `projectId`          | `integer` | Id of the project the collaborator is on.           |
| `collaboratorUserId` | `string`  | User Id of the collaborator to update.              |
| `liveControl`        | `boolean` | Gives the right to deploy and stop live algorithms. |
| `write`              | `boolean` | Gives the right to edit the code.                   |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `delete_project_collaborator`

Remove a collaborator from a project.

| Parameter        | Type      | Description                                        |
| ---------------- | --------- | -------------------------------------------------- |
| `projectId`      | `integer` | Id of the project to remove the collaborator from. |
| `collaboratorId` | `string`  | User Id of the collaborator to remove.             |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `lock_project_with_collaborators`

Lock a project so you can edit it.

| Parameter      | Type      | Description                                          |
| -------------- | --------- | ---------------------------------------------------- |
| `projectId`    | `integer` | Id of the project to edit.                           |
| `codeSourceId` | `string`  | Name of the environment that's creating the request. |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_project_nodes`

Read the available and selected nodes of a project.

| Parameter   | Type      | Description                                 |
| ----------- | --------- | ------------------------------------------- |
| `projectId` | `integer` | Id of the project to which the nodes refer. |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `update_project_nodes`

Update the active state of the given nodes to true.

| Parameter   | Type               | Description                                                                                                                                                                   |
| ----------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `projectId` | `integer`          | Project Id to which the nodes refer.                                                                                                                                          |
| `nodes`     | `array` _optional_ | List of node Ids the project may use. If you omit this property or pass an empty list, the best node will be automatically selected for backtest, research, and live trading. |

_This tool modifies it's environment._

_This tool doesn't perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `create_compile`

Asynchronously create a compile job request for a project.

| Parameter   | Type      | Description                   |
| ----------- | --------- | ----------------------------- |
| `projectId` | `integer` | Id of the project to compile. |

_This tool modifies it's environment._

_This tool doesn't perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_compile`

Read a compile packet job result.

| Parameter   | Type      | Description                                      |
| ----------- | --------- | ------------------------------------------------ |
| `projectId` | `integer` | Id of the project you requested to compile.      |
| `compileId` | `string`  | Compile Id returned during the creation request. |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `create_file`

Add a file to a given project.

| Parameter      | Type                | Description                                          |
| -------------- | ------------------- | ---------------------------------------------------- |
| `projectId`    | `integer`           | Id of the project to add the file.                   |
| `name`         | `string`            | The name of the new file.                            |
| `content`      | `string` _optional_ | The content of the new file.                         |
| `codeSourceId` | `string` _optional_ | Name of the environment that's creating the request. |

_This tool modifies it's environment._

_This tool doesn't perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_file`

Read a file from a project, or all files in the project if no file name is provided.

| Parameter      | Type                | Description                                          |
| -------------- | ------------------- | ---------------------------------------------------- |
| `projectId`    | `integer`           | Id of the project that contains the file.            |
| `name`         | `string` _optional_ | The name of the file to read.                        |
| `codeSourceId` | `string` _optional_ | Name of the environment that's creating the request. |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `update_file_name`

Update the name of a file.

| Parameter      | Type                | Description                                          |
| -------------- | ------------------- | ---------------------------------------------------- |
| `projectId`    | `integer`           | Id of the project that contains the file.            |
| `name`         | `string`            | The current name of the file.                        |
| `newName`      | `string`            | The new name for the file.                           |
| `codeSourceId` | `string` _optional_ | Name of the environment that's creating the request. |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `update_file_contents`

Update the contents of a file.

| Parameter      | Type                | Description                                          |
| -------------- | ------------------- | ---------------------------------------------------- |
| `projectId`    | `integer`           | Id of the project that contains the file.            |
| `name`         | `string`            | The name of the file to update.                      |
| `content`      | `string`            | The new contents of the file.                        |
| `codeSourceId` | `string` _optional_ | Name of the environment that's creating the request. |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `patch_file`

Apply a patch (unified diff) to a file in a project.

| Parameter      | Type                | Description                                                                                                                               |
| -------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `projectId`    | `integer`           | Id of the project that contains the file.                                                                                                 |
| `patch`        | `string`            | A patch string in **unified diff format** (as produced by `git diff`). It specifies changes to apply to one or more files in the project. |
| `codeSourceId` | `string` _optional_ | Name of the environment that's creating the request.                                                                                      |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `delete_file`

Delete a file in a project.

| Parameter      | Type                | Description                                          |
| -------------- | ------------------- | ---------------------------------------------------- |
| `projectId`    | `integer`           | Id of the project that contains the file.            |
| `name`         | `string`            | The name of the file to delete.                      |
| `codeSourceId` | `string` _optional_ | Name of the environment that's creating the request. |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `create_backtest`

Create a new backtest request and get the backtest Id.

| Parameter      | Type                | Description                             |
| -------------- | ------------------- | --------------------------------------- |
| `projectId`    | `integer`           | Id of the project to backtest.          |
| `compileId`    | `string`            | Compile Id for the project to backtest. |
| `backtestName` | `string`            | Name for the new backtest.              |
| `parameters`   | `object` _optional_ | Parameters to use for the backtest.     |

_This tool modifies it's environment._

_This tool doesn't perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `create_backtest_brief` ⚡

Create a new backtest request and get only the essential fields (backtestId and status).

| Parameter      | Type                | Description                             |
| -------------- | ------------------- | --------------------------------------- |
| `projectId`    | `integer`           | Id of the project to backtest.          |
| `compileId`    | `string`            | Compile Id for the project to backtest. |
| `backtestName` | `string`            | Name for the new backtest.              |
| `parameters`   | `object` _optional_ | Parameters to use for the backtest.     |

_This tool modifies it's environment._

_This tool doesn't perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

**Note:** This is a token-optimized version that returns only `backtestId` and `status` fields instead of the full backtest object, reducing response size by 90%+ for improved LLM performance.

---

**Tool:** `read_backtest`

Read the results of a backtest.

| Parameter    | Type      | Description                                   |
| ------------ | --------- | --------------------------------------------- |
| `projectId`  | `integer` | Id of the project that contains the backtest. |
| `backtestId` | `string`  | Id of the backtest to read.                   |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_backtest_brief` ⚡

Read a brief summary of backtest results containing only status, error, and hasInitializeError.

| Parameter    | Type      | Description                                   |
| ------------ | --------- | --------------------------------------------- |
| `projectId`  | `integer` | Id of the project that contains the backtest. |
| `backtestId` | `string`  | Id of the backtest to read.                   |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

**Note:** This is a token-optimized version that returns only `status`, `error`, and `hasInitializeError` fields instead of the full backtest result object, reducing response size by 90%+ for improved LLM performance.

---

**Tool:** `wait_for_backtest` ⚡

Poll for backtest completion with configurable timeout and interval.

| Parameter         | Type      | Description                                                              |
| ----------------- | --------- | ------------------------------------------------------------------------ |
| `projectId`       | `integer` | Id of the project that contains the backtest.                           |
| `backtestId`      | `string`  | Id of the backtest to read.                                              |
| `max_timeout`     | `integer` | Maximum time to wait in seconds (default: 90, max: 120).                |
| `polling_interval`| `integer` | Time between polls in seconds (default: 10, min: 5).                    |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

**Note:** This tool efficiently polls for backtest completion, returning immediately when the backtest finishes or timing out after the specified duration. Returns elapsed time information in the errors field.

---

**Tool:** `read_backtest_statistics` ⚡

Read key performance statistics from backtest results.

| Parameter    | Type      | Description                                   |
| ------------ | --------- | --------------------------------------------- |
| `projectId`  | `integer` | Id of the project that contains the backtest. |
| `backtestId` | `string`  | Id of the backtest to read.                   |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

**Note:** This is a token-optimized version that returns ~20 key statistics including Total Return, Sharpe Ratio, Drawdown, Win Rate, and portfolio performance metrics, reducing response size by 80%+ compared to the full backtest results.

---

**Tool:** `list_backtests`

List all the backtests for the project.

| Parameter           | Type                 | Description                                                                                                     |
| ------------------- | -------------------- | --------------------------------------------------------------------------------------------------------------- |
| `projectId`         | `integer`            | Id of the project from which to read one or multiple backtests.                                                 |
| `includeStatistics` | `boolean` _optional_ | If true, the backtests summaries from the response will contain the statistics with their corresponding values. |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_backtest_chart`

Read a chart from a backtest.

| Parameter    | Type      | Description                                      |
| ------------ | --------- | ------------------------------------------------ |
| `projectId`  | `integer` | Id of the project that contains the backtest.    |
| `backtestId` | `string`  | Id of the backtest for this chart request.       |
| `name`       | `string`  | The requested chart name.                        |
| `count`      | `integer` | The number of data points to request.            |
| `start`      | `integer` | The start timestamp of the request in Unix time. |
| `end`        | `integer` | The end timestamp of the request in Unix time.   |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_backtest_orders`

Read out the orders of a backtest.

| Parameter    | Type      | Description                                                                          |
| ------------ | --------- | ------------------------------------------------------------------------------------ |
| `start`      | `integer` | Starting index of the orders to be fetched.                                          |
| `end`        | `integer` | Last index of the orders to be fetched. Note that end - start must be less than 100. |
| `projectId`  | `integer` | Id of the project from which to read the backtest.                                   |
| `backtestId` | `string`  | Id of the backtest from which to read the orders.                                    |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_backtest_insights`

Read out the insights of a backtest.

| Parameter    | Type      | Description                                                                            |
| ------------ | --------- | -------------------------------------------------------------------------------------- |
| `start`      | `integer` | Starting index of the insights to be fetched.                                          |
| `end`        | `integer` | Last index of the insights to be fetched. Note that end - start must be less than 100. |
| `projectId`  | `integer` | Id of the project from which to read the backtest.                                     |
| `backtestId` | `string`  | Id of the backtest from which to read the insights.                                    |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `update_backtest`

Update the name or note of a backtest.

| Parameter    | Type                | Description                                   |
| ------------ | ------------------- | --------------------------------------------- |
| `projectId`  | `integer`           | Id of the project that contains the backtest. |
| `backtestId` | `string`            | Id of the backtest to update.                 |
| `note`       | `string` _optional_ | Note to attach to the backtest.               |
| `name`       | `string` _optional_ | Name to assign to the backtest.               |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `delete_backtest`

Delete a backtest from a project.

| Parameter    | Type      | Description                                   |
| ------------ | --------- | --------------------------------------------- |
| `projectId`  | `integer` | Id of the project that contains the backtest. |
| `backtestId` | `string`  | Id of the backtest to delete.                 |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `estimate_optimization_time`

Estimate the execution time of an optimization with the specified parameters.

| Parameter     | Type                | Description                                                   |
| ------------- | ------------------- | ------------------------------------------------------------- |
| `projectId`   | `integer`           | Id of the project to optimize.                                |
| `name`        | `string`            | Name of the optimization.                                     |
| `target`      | `string`            | Target statistic of the optimization to minimize or maximize. |
| `targetTo`    | `string`            | Target extremum of the optimization.                          |
| `targetValue` | `number` _optional_ | Desired value for the optimization target statistic.          |
| `strategy`    | `string`            | Optimization strategy.                                        |
| `compileId`   | `string` _optional_ | Optimization compile Id.                                      |
| `parameters`  | `array`             | Optimization parameters.                                      |
| `constraints` | `array` _optional_  | Optimization constraints.                                     |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `create_optimization`

Create an optimization with the specified parameters.

| Parameter       | Type                | Description                                                   |
| --------------- | ------------------- | ------------------------------------------------------------- |
| `projectId`     | `integer`           | Id of the project to optimize.                                |
| `name`          | `string`            | Name of the optimization.                                     |
| `target`        | `string`            | Target statistic of the optimization to minimize or maximize. |
| `targetTo`      | `string`            | Target extremum of the optimization.                          |
| `targetValue`   | `number` _optional_ | Desired value for the optimization target statistic.          |
| `strategy`      | `string`            | Optimization strategy.                                        |
| `compileId`     | `string`            | Optimization compile Id.                                      |
| `parameters`    | `array`             | Optimization parameters.                                      |
| `constraints`   | `array` _optional_  | Optimization constraints.                                     |
| `estimatedCost` | `number`            | Estimated cost for optimization.                              |
| `nodeType`      | `string`            | Optimization node type.                                       |
| `parallelNodes` | `integer`           | Number of parallel nodes for optimization.                    |

_This tool modifies it's environment._

_This tool doesn't perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_optimization`

Read an optimization.

| Parameter        | Type     | Description                     |
| ---------------- | -------- | ------------------------------- |
| `optimizationId` | `string` | Id of the optimization to read. |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `list_optimizations`

List all the optimizations for a project.

| Parameter   | Type      | Description                                           |
| ----------- | --------- | ----------------------------------------------------- |
| `projectId` | `integer` | Id of the Project to get a list of optimizations for. |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `update_optimization`

Update the name of an optimization.

| Parameter        | Type     | Description                         |
| ---------------- | -------- | ----------------------------------- |
| `optimizationId` | `string` | Id of the optimization to update.   |
| `name`           | `string` | Name to assign to the optimization. |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `abort_optimization`

Abort an optimization.

| Parameter        | Type     | Description                      |
| ---------------- | -------- | -------------------------------- |
| `optimizationId` | `string` | Id of the optimization to abort. |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `delete_optimization`

Delete an optimization.

| Parameter        | Type     | Description                       |
| ---------------- | -------- | --------------------------------- |
| `optimizationId` | `string` | Id of the optimization to delete. |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `authorize_connection`

Authorize an external connection with a live brokerage or data provider.

| Parameter   | Type     | Description                                      |
| ----------- | -------- | ------------------------------------------------ |
| `brokerage` | `string` | The brokerage to authenticate a connection with. |

_This tool modifies it's environment._

_This tool doesn't perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `create_live_algorithm`

Create a live algorithm.

| Parameter       | Type                | Description                                                                                                                                                                                                                     |
| --------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `versionId`     | `string`            | The version of the Lean used to run the algorithm. -1 is master, however, sometimes this can create problems with live deployments. If you experience problems using, try specifying the version of Lean you would like to use. |
| `projectId`     | `integer`           | Project Id.                                                                                                                                                                                                                     |
| `compileId`     | `string`            | Compile Id.                                                                                                                                                                                                                     |
| `nodeId`        | `string`            | Id of the node that will run the algorithm.                                                                                                                                                                                     |
| `brokerage`     | `object`            | Brokerage configuration for the live algorithm.                                                                                                                                                                                 |
| `dataProviders` | `object` _optional_ | Dictionary of data provider configurations to be used in the live algorithm. Provide at least one. The order in which you define the providers defines their order of precedence.                                               |

_This tool modifies it's environment._

_This tool doesn't perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_live_algorithm`

Read details of a live algorithm.

| Parameter   | Type      | Description                |
| ----------- | --------- | -------------------------- |
| `projectId` | `integer` | Id of the project to read. |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `list_live_algorithms`

List all your past and current live trading deployments.

| Parameter   | Type                     | Description                                                                                                                              |
| ----------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `projectId` | `integer` _optional_     | Id of the project to include in response. If you omit this property, the response includes all your projects.                            |
| `status`    | `status enum` _optional_ | Status of the live deployments to include in the response. If you omit this property, the response includes deployments with any status. |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_live_chart`

Read a chart from a live algorithm.

| Parameter   | Type      | Description                            |
| ----------- | --------- | -------------------------------------- |
| `projectId` | `integer` | Id of the project that's live trading. |
| `name`      | `string`  | Name of the chart to read.             |
| `count`     | `integer` | The number of data points to request.  |
| `start`     | `integer` | The unix start time of the request.    |
| `end`       | `integer` | The unix end time of the request.      |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_live_logs`

Get the logs of a live algorithm.

| Parameter     | Type          | Description                                                             |
| ------------- | ------------- | ----------------------------------------------------------------------- |
| `format`      | `` _optional_ | Format of the log results.                                              |
| `projectId`   | `integer`     | Id of the project that contains the live running algorithm.             |
| `algorithmId` | `string`      | Deploy Id (Algorithm Id) of the live running algorithm.                 |
| `startLine`   | `integer`     | Start line (inclusive) of logs to read. The lines numbers start at 0.   |
| `endLine`     | `integer`     | End line (exclusive) of logs to read, where endLine - startLine <= 250. |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_live_portfolio`

Read out the portfolio state of a live algorithm.

| Parameter   | Type      | Description                                              |
| ----------- | --------- | -------------------------------------------------------- |
| `projectId` | `integer` | Id of the project from which to read the live algorithm. |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_live_orders`

Read out the orders of a live algorithm.

| Parameter   | Type      | Description                                                                     |
| ----------- | --------- | ------------------------------------------------------------------------------- |
| `start`     | `integer` | Starting index of the orders to be fetched.                                     |
| `end`       | `integer` | Last index of the orders to be fetched. Note that end - start must be <= 1,000. |
| `projectId` | `integer` | Id of the project from which to read the live algorithm.                        |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_live_insights`

Read out the insights of a live algorithm.

| Parameter   | Type                 | Description                                                                            |
| ----------- | -------------------- | -------------------------------------------------------------------------------------- |
| `start`     | `integer` _optional_ | Starting index of the insights to be fetched. Required if end > 100.                   |
| `end`       | `integer`            | Last index of the insights to be fetched. Note that end - start must be less than 100. |
| `projectId` | `integer`            | Id of the project from which to read the live algorithm.                               |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `stop_live_algorithm`

Stop a live algorithm.

| Parameter   | Type      | Description                             |
| ----------- | --------- | --------------------------------------- |
| `projectId` | `integer` | Id of the project to stop trading live. |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `liquidate_live_algorithm`

Liquidate and stop a live algorithm.

| Parameter   | Type      | Description                                    |
| ----------- | --------- | ---------------------------------------------- |
| `projectId` | `integer` | Project Id for the live instance to liquidate. |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `create_live_command`

Send a command to a live trading algorithm.

| Parameter   | Type      | Description                                                       |
| ----------- | --------- | ----------------------------------------------------------------- |
| `projectId` | `integer` | Project for the live instance we want to run the command against. |
| `command`   | `object`  | The command to run.                                               |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `broadcast_live_command`

Broadcast a live command to all live algorithms in an organization.

| Parameter          | Type                 | Description                                                                                                       |
| ------------------ | -------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `organizationId`   | `string`             | Organization Id of the projects we would like to broadcast the command to                                         |
| `excludeProjectId` | `integer` _optional_ | Project for the live instance we want to exclude from the broadcast list. If null, all projects will be included. |
| `command`          | `object`             | The command to run.                                                                                               |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `upload_object`

Upload files to the Object Store.

| Parameter        | Type     | Description                                      |
| ---------------- | -------- | ------------------------------------------------ |
| `organizationId` | `string` | Orgainization ID.                                |
| `key`            | `string` | Unique key to access the object in Object Store. |
| `objectData`     | `string` | Object data to be stored.                        |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_object_properties`

Get Object Store properties of a specific organization and key.

| Parameter        | Type     | Description                                        |
| ---------------- | -------- | -------------------------------------------------- |
| `organizationId` | `string` | Id of the organization that owns the Object Store. |
| `key`            | `string` | Key in the Object Store.                           |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_object_store_file_job_id`

Create a job to download files from the Object Store and then read the job Id.

| Parameter        | Type     | Description                                        |
| ---------------- | -------- | -------------------------------------------------- |
| `organizationId` | `string` | Id of the organization that owns the Object Store. |
| `keys`           | `array`  | Keys of the Object Store files.                    |

_This tool modifies it's environment._

_This tool doesn't perform destructive updates._

_Calling this tool repeatedly with the same arguments has additional effects._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_object_store_file_download_url`

Get the URL for downloading files from the Object Store.

| Parameter        | Type     | Description                                        |
| ---------------- | -------- | -------------------------------------------------- |
| `organizationId` | `string` | Id of the organization that owns the Object Store. |
| `jobId`          | `string` | Id of the download job for the files.              |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `list_object_store_files`

List the Object Store files under a specific directory in an organization.

| Parameter        | Type                | Description                                                 |
| ---------------- | ------------------- | ----------------------------------------------------------- |
| `organizationId` | `string`            | Id of the organization to list the Object Store files from. |
| `path`           | `string` _optional_ | Path to a directory in the Object Store.                    |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `delete_object`

Delete the Object Store file of a specific organization and key.

| Parameter        | Type     | Description                                        |
| ---------------- | -------- | -------------------------------------------------- |
| `organizationId` | `string` | Id of the organization that owns the Object Store. |
| `key`            | `string` | Key of the Object Store file to delete.            |

_This tool modifies it's environment._

_This tool may perform destructive updates._

_Calling this tool repeatedly with the same arguments has no additional effect._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_lean_versions`

Returns a list of LEAN versions with basic information for each version.

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `check_initialization_errors`

Run a backtest for a few seconds to initialize the algorithm and get inialization errors if any.

| Parameter  | Type     | Description           |
| ---------- | -------- | --------------------- |
| `language` | `string` | Programming language. |
| `files`    | `array`  | Files to process.     |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `complete_code`

Show the code completion for a specific text input.

| Parameter           | Type                 | Description                                   |
| ------------------- | -------------------- | --------------------------------------------- |
| `language`          | `string`             | Programming language for the code completion. |
| `sentence`          | `string`             | Sentence to complete.                         |
| `responseSizeLimit` | `integer` _optional_ | Maximum size of the responses.                |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `enhance_error_message`

Show additional context and suggestions for error messages.

| Parameter  | Type     | Description                                   |
| ---------- | -------- | --------------------------------------------- |
| `language` | `string` | Programming language for the code completion. |
| `error`    | `object` | Error message to enhance.                     |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `update_code_to_pep8`

Update Python code to follow PEP8 style.

| Parameter | Type    | Description           |
| --------- | ------- | --------------------- |
| `files`   | `array` | Files of the project. |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `check_syntax`

Check the syntax of a code.

| Parameter  | Type     | Description           |
| ---------- | -------- | --------------------- |
| `language` | `string` | Programming language. |
| `files`    | `array`  | Files to process.     |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `search_quantconnect`

Search for content in QuantConnect.

| Parameter  | Type     | Description                                    |
| ---------- | -------- | ---------------------------------------------- |
| `language` | `string` | Programming language of the content to search. |
| `criteria` | `array`  | Criteria for the search.                       |

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_mcp_server_version`

Returns the version of the QC MCP Server that's running.

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

**Tool:** `read_latest_mcp_server_version`

Returns the latest version of the QC MCP Server released.

_This tool doesn't modify it's environment._

_This tool may interact with an "open world" of external entities._

---

## Debugging

### Build

To build the Docker image from source, clone this repository and then run `docker build -t quantconnect/mcp-server .`.

### Logs

To log to the `mcp-server-quantconnect.log` file, `import sys` and then `print("Hello world", file=sys.stderr)`.

### Inspector

To start the inspector, run `npx @modelcontextprotocol/inspector uv run src/main.py`.
To pass a model to the inspector tool, use JSON (for example, `{"name":"My Project","language":"Py"}`).
