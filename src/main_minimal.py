import logging
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Import only the tools we need for the minimal server
from api_connection import post
from code_source_id import add_code_source_id
from models import (
    # File operations
    ReadFilesRequest,
    UpdateFileContentsRequest,
    ProjectFilesResponse,
    # Compile operations
    CreateCompileRequest,
    ReadCompileRequest,
    CreateCompileResponse,
    ReadCompileResponse,
    # Backtest operations
    CreateBacktestRequest,
    ReadBacktestRequest,
    BacktestResponse,
    # AI operations
    SearchRequest,
    SearchResponse,
)
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
            f"{log_dir}/quantconnect-mcp-minimal.log", mode="a"
        ),  # Append to log file
    ],
)
logger = logging.getLogger("quantconnect-mcp-minimal")

# Log startup information (before any tool registration)
logger.info("=" * 60)
logger.info("🚀 QuantConnect MCP MINIMAL Server Starting Up")
logger.info(f"⏰ Startup time: {datetime.now().isoformat()}")
logger.info(f"🌐 Transport: {os.getenv('MCP_TRANSPORT', 'stdio')}")
logger.info(f"📍 Host: {os.getenv('MCP_HOST', '127.0.0.1')}")
logger.info(f"🔌 Port: {os.getenv('MCP_PORT', '8000')}")
logger.info(f"👤 User ID: {os.getenv('QUANTCONNECT_USER_ID', 'Not set')}")
logger.info(
    f"🔑 API Token: {'✅ Set' if os.getenv('QUANTCONNECT_API_TOKEN') else '❌ Not set'}"
)
logger.info("🔧 MINIMAL SERVER - Only 8 tools exposed")
logger.info("=" * 60)

# Get configuration from environment variables
transport = os.getenv("MCP_TRANSPORT", "stdio")
host = os.getenv("MCP_HOST", "127.0.0.1")
port = int(os.getenv("MCP_PORT", "8000"))

# Load the server instructions.
with open("src/instructions_minimal.md", "r", encoding="utf-8") as file:
    instructions = file.read()

logger.info(f"🔧 Initializing FastMCP minimal server with host={host}, port={port}")

# Initialize the FastMCP server with host and port configuration.
mcp = FastMCP("quantconnect-minimal", instructions, host=host, port=port)

logger.info("📋 Starting MINIMAL tool registration process...")


# Register only the 8 specified tools
def register_minimal_tools(mcp):
    """Register only the 8 essential tools for the minimal server."""

    # 1. read_file
    @mcp.tool(annotations={"title": "Read file", "readOnlyHint": True})
    async def read_file(model: ReadFilesRequest) -> ProjectFilesResponse:
        """Read a file from a project, or all files in the project if
        no file name is provided.
        """
        return await post("/files/read", add_code_source_id(model))

    # 2. update_file_contents
    @mcp.tool(annotations={"title": "Update file contents", "idempotentHint": True})
    async def update_file_contents(
        model: UpdateFileContentsRequest,
    ) -> ProjectFilesResponse:
        """Update the contents of a file."""
        return await post("/files/update", add_code_source_id(model))

    # 3. create_compile
    @mcp.tool(annotations={"title": "Create compile", "destructiveHint": False})
    async def create_compile(model: CreateCompileRequest) -> CreateCompileResponse:
        """Asynchronously create a compile job request for a project."""
        return await post("/compile/create", model)

    # 4. read_compile
    @mcp.tool(annotations={"title": "Read compile", "readOnlyHint": True})
    async def read_compile(model: ReadCompileRequest) -> ReadCompileResponse:
        """Read a compile packet job result."""
        return await post("/compile/read", model)

    # 5. create_backtest_brief
    @mcp.tool(annotations={"title": "Create backtest brief", "destructiveHint": False})
    async def create_backtest_brief(model: CreateBacktestRequest) -> BacktestResponse:
        """Create a new backtest request and get only the essential fields (backtestId and status)."""
        response = await post("/backtests/create", model)
        # Create a simplified response with only the essential fields
        if "backtestId" in response and "status" in response:
            return {
                "backtestId": response["backtestId"],
                "status": response["status"],
                "success": response.get("success", True),
            }
        return response

    # 6. read_backtest_brief
    @mcp.tool(annotations={"title": "Read backtest brief", "readOnlyHint": True})
    async def read_backtest_brief(model: ReadBacktestRequest) -> BacktestResponse:
        """Read a brief summary of backtest results containing only status, error, and hasInitializeError."""
        response = await post("/backtests/read", model)
        # Create a simplified response with only the required fields
        brief_response = {"success": response.get("success", False)}

        if "status" in response:
            brief_response["status"] = response["status"]
        if "error" in response:
            brief_response["error"] = response["error"]
        if "hasInitializeError" in response:
            brief_response["hasInitializeError"] = response["hasInitializeError"]

        return brief_response

    # 7. read_backtest_statistics
    @mcp.tool(annotations={"title": "Read backtest statistics", "readOnlyHint": True})
    async def read_backtest_statistics(model: ReadBacktestRequest) -> BacktestResponse:
        """Read key performance statistics from backtest results."""
        response = await post("/backtests/read", model)
        # Create a simplified response with only the key statistics
        stats_response = {"success": response.get("success", False)}

        if "statistics" in response:
            # Include only essential performance metrics
            essential_stats = {}
            stats = response["statistics"]

            # Key performance metrics
            key_metrics = [
                "TotalPerformance.PortfolioStatistics.SharpeRatio",
                "TotalPerformance.PortfolioStatistics.CompoundingAnnualReturn",
                "TotalPerformance.PortfolioStatistics.Drawdown",
                "TotalPerformance.PortfolioStatistics.TotalReturn",
                "TotalPerformance.PortfolioStatistics.TotalTrades",
                "TotalPerformance.PortfolioStatistics.WinRate",
                "TotalPerformance.PortfolioStatistics.ProfitLossRatio",
            ]

            for metric in key_metrics:
                if metric in stats:
                    essential_stats[metric] = stats[metric]

            stats_response["statistics"] = essential_stats

        return stats_response

    # 8. search_quantconnect
    @mcp.tool(annotations={"title": "Search QuantConnect", "readOnlyHint": True})
    async def search_quantconnect(model: SearchRequest) -> SearchResponse:
        """Search for content in QuantConnect."""
        return await post("/ai/tools/search", model)

    logger.info("✅ Registered 8 essential tools for minimal server")


# Register the minimal tools
register_minimal_tools(mcp)

logger.info("✅ MINIMAL tool registration process completed successfully")
logger.info(
    "🔒 Security: Only 8 essential tools exposed (88% reduction from full server)"
)

if __name__ == "__main__":
    # Load the organization workspace.
    OrganizationWorkspace.load()
    # Run the server.

    if transport == "streamable-http" or transport == "http":
        logger.info(
            f"🌐 Starting QuantConnect MCP MINIMAL Server with HTTP transport on {host}:{port}"
        )
        logger.info(f"📡 MCP endpoint: http://{host}:{port}/mcp")
        logger.info("🔄 Server is running - Press Ctrl+C to stop")
        print(
            f"🌐 Starting QuantConnect MCP MINIMAL Server with HTTP transport on {host}:{port}"
        )
        print(f"   MCP endpoint: http://{host}:{port}/mcp")
        print("   Press Ctrl+C to stop the server")
        mcp.run(transport="streamable-http")
    else:
        logger.info("📡 Starting QuantConnect MCP MINIMAL Server with stdio transport")
        logger.info("🔄 Server is running")
        # Default stdio transport for MCP clients like Claude Desktop
        print("📡 Starting QuantConnect MCP MINIMAL Server with stdio transport")
        mcp.run(transport="stdio")
