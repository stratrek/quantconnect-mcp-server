from src import __version__

def register_mcp_server_version_tools(mcp):
    # Read
    @mcp.tool(
        annotations={
            'title': 'Read QC MCP Server version', 'readOnlyHint': True
        }
    )
    async def read_mcp_server_version() -> str:
        """Returns the version of the QC MCP Server that's running."""
        return __version__
