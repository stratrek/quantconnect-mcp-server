# mcp-server
Python MCP server for local interactions with the QuantConnect API. 


## Configuration Examples
To connect local MCP clients (like Claude Desktop) to the QC MCP Server, add the following JSON to your configuration file:
```
{
  "mcpServers": {
    "quantconnect": {
      "command": "uv",
      "args": [
        "--directory",
        "your\\path\\to\\quantconnect\\mcp-server",
        "run",
        "src/main.py"
      ],
      "env": {
        "QUANTCONNECT_USER_ID": <your_user_id>,
        "QUANTCONNECT_API_TOKEN": "<your_api_token"
      }
    }
  }
}
```

## Debugging

### Logs
 To log to the `mcp-server-quantconnect.log` file, `import sys` and then `print("Hello world", file=sys.stderr)`.

### Inspector
 To start the inspector, run `npx @modelcontextprotocol/inspector uv run main.py`.
 To pass a model to the inspector tool, use JSON (for example, `{"name":"My Project","language":"Py"}`).
