import logging
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

from tools.account import register_account_tools
from tools.project import register_project_tools
from tools.project_collaboration import register_project_collaboration_tools
from tools.project_nodes import register_project_node_tools
from tools.compile import register_compile_tools
from tools.files import register_file_tools
from tools.backtests import register_backtest_tools
from tools.optimizations import register_optimization_tools
from tools.live import register_live_trading_tools
from tools.live_commands import register_live_trading_command_tools
from tools.object_store import register_object_store_tools
from tools.lean_versions import register_lean_version_tools
from tools.ai import register_ai_tools
from tools.mcp_server_version import register_mcp_server_version_tools
from organization_workspace import OrganizationWorkspace

# Configure logging before any other imports
# Create logs directory if it doesn't exist
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Set up logging with both console and file output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Console output (captured by systemd)
        logging.FileHandler(
            f"{log_dir}/quantconnect-mcp.log", mode="a"
        ),  # Append to log file
    ],
)
logger = logging.getLogger("quantconnect-mcp")

# Log startup information (before any tool registration)
logger.info("=" * 60)
logger.info("🚀 QuantConnect MCP Server Starting Up")
logger.info(f"⏰ Startup time: {datetime.now().isoformat()}")
logger.info(f"🌐 Transport: {os.getenv('MCP_TRANSPORT', 'stdio')}")
logger.info(f"📍 Host: {os.getenv('MCP_HOST', '127.0.0.1')}")
logger.info(f"🔌 Port: {os.getenv('MCP_PORT', '8000')}")
logger.info(f"👤 User ID: {os.getenv('QUANTCONNECT_USER_ID', 'Not set')}")
logger.info(
    f"🔑 API Token: {'✅ Set' if os.getenv('QUANTCONNECT_API_TOKEN') else '❌ Not set'}"
)
logger.info("=" * 60)

# Get configuration from environment variables
transport = os.getenv("MCP_TRANSPORT", "stdio")
host = os.getenv("MCP_HOST", "127.0.0.1")
port = int(os.getenv("MCP_PORT", "8000"))

# Load the server instructions.
with open("src/instructions.md", "r", encoding="utf-8") as file:
    instructions = file.read()

logger.info(f"🔧 Initializing FastMCP server with host={host}, port={port}")

# Initialize the FastMCP server with host and port configuration.
mcp = FastMCP("quantconnect", instructions, host=host, port=port)

logger.info("📋 Starting tool registration process...")

# Register all the tools.
registration_functions = [
    register_account_tools,
    register_project_tools,
    register_project_collaboration_tools,
    register_project_node_tools,
    register_compile_tools,
    register_file_tools,
    register_backtest_tools,
    register_optimization_tools,
    register_live_trading_tools,
    register_live_trading_command_tools,
    register_object_store_tools,
    register_lean_version_tools,
    register_ai_tools,
    register_mcp_server_version_tools,
]
for f in registration_functions:
    f(mcp)

logger.info("✅ Tool registration process completed successfully")

if __name__ == "__main__":
    # Load the organization workspace.
    OrganizationWorkspace.load()
    # Run the server.

    if transport == "streamable-http" or transport == "http":
        logger.info(
            f"🌐 Starting QuantConnect MCP Server with HTTP transport on {host}:{port}"
        )
        logger.info(f"📡 MCP endpoint: http://{host}:{port}/mcp")
        logger.info("🔄 Server is running - Press Ctrl+C to stop")
        print(
            f"🌐 Starting QuantConnect MCP Server with HTTP transport on {host}:{port}"
        )
        print(f"   MCP endpoint: http://{host}:{port}/mcp")
        print("   Press Ctrl+C to stop the server")
        mcp.run(transport="streamable-http")
    else:
        logger.info("📡 Starting QuantConnect MCP Server with stdio transport")
        logger.info("🔄 Server is running")
        # Default stdio transport for MCP clients like Claude Desktop
        print("📡 Starting QuantConnect MCP Server with stdio transport")
        mcp.run(transport="stdio")
