# mcp-server
Python MCP server for local interactions with the QuantConnect API. 


## Debugging

### Logs
 To log to the `mcp-server-quantconnect.log` file, `import sys` and then `print("Hello world", file=sys.stderr)`.

### Inspector
 To start the inspector, run `npx @modelcontextprotocol/inspector uv run main.py`.
 To pass a model to the inspector tool, use JSON (for example, `{"name":"My Project","language":"Py"}`).
