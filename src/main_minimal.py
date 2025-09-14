import logging
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Import dependencies for the 9 minimal tools
from api_connection import post
from code_source_id import add_code_source_id
from models import (
    # Project operations
    CreateProjectRequest,
    ProjectListResponse,
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
    BacktestResult,
    StatisticsResult,
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
logger.info("🔧 MINIMAL SERVER - Only 9 tools exposed")
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


def register_minimal_tools(mcp):
    """Register only the 9 essential tools for the minimal server.
    Each tool is copied exactly from its original implementation.
    """

    # 1. create_project (from tools/project.py)
    @mcp.tool(
        annotations={
            'title': 'Create project',
            'destructiveHint': False,
            'idempotentHint': False
        }
    )
    async def create_project(model: CreateProjectRequest) -> ProjectListResponse:
        """Create a new project in your default organization."""
        return await post('/projects/create', model)

    # 2. read_file (from tools/files.py)
    @mcp.tool(annotations={'title': 'Read file', 'readOnlyHint': True})
    async def read_file(model: ReadFilesRequest) -> ProjectFilesResponse:
        """Read a file from a project, or all files in the project if
        no file name is provided.
        """
        return await post('/files/read', add_code_source_id(model))

    # 3. update_file_contents (from tools/files.py)
    @mcp.tool(
        annotations={'title': 'Update file contents', 'idempotentHint': True}
    )
    async def update_file_contents(
            model: UpdateFileContentsRequest) -> ProjectFilesResponse:
        """Update the contents of a file."""
        return await post('/files/update', add_code_source_id(model))

    # 4. create_compile (from tools/compile.py)
    @mcp.tool(
        annotations={'title': 'Create compile', 'destructiveHint': False}
    )
    async def create_compile(
            model: CreateCompileRequest) -> CreateCompileResponse:
        """Asynchronously create a compile job request for a project."""
        return await post('/compile/create', model)

    # 5. read_compile (from tools/compile.py)
    @mcp.tool(annotations={'title': 'Read compile', 'readOnlyHint': True})
    async def read_compile(model: ReadCompileRequest) -> ReadCompileResponse:
        """Read a compile packet job result."""
        return await post('/compile/read', model)

    # 6. create_backtest_brief (from tools/backtests.py)
    @mcp.tool(annotations={"title": "Create backtest brief", "destructiveHint": False})
    async def create_backtest_brief(model: CreateBacktestRequest) -> BacktestResponse:
        """Create a new backtest request and get only the essential fields (backtestId and status)."""
        response = await post("/backtests/create", model)

        # Create a simplified response with only the essential fields
        # The API response is a dict, not an object with attributes
        # Must check success=True before proceeding
        if (
            isinstance(response, dict)
            and response.get("success")
            and "backtest" in response
            and response["backtest"]
        ):
            backtest_data = response["backtest"]
            simplified_result = BacktestResult(
                backtestId=backtest_data["backtestId"], status=backtest_data["status"]
            )

            # Return the simplified response
            return BacktestResponse(
                backtest=simplified_result,
                success=response["success"],
                errors=response.get("errors", []),
            )

        # If API call failed or no backtest data, return actual errors from API
        api_errors = []
        if isinstance(response, dict):
            # Extract errors from API response if available
            api_errors = response.get("errors", [])
            if not api_errors and not response.get("success"):
                api_errors = ["API call failed but no specific error provided"]

        if not api_errors:
            api_errors = ["No backtest data available"]

        return BacktestResponse(backtest=None, success=False, errors=api_errors)

    # 7. read_backtest_brief (from tools/backtests.py)
    @mcp.tool(annotations={"title": "Read backtest brief", "readOnlyHint": True})
    async def read_backtest_brief(model: ReadBacktestRequest) -> BacktestResponse:
        """Read a brief summary of backtest results containing only status, error, and hasInitializeError."""
        response = await post("/backtests/read", model)

        # Create a simplified response with only the required fields
        # The API response is a dict, not an object with attributes
        # Must check success=True before proceeding
        if (
            isinstance(response, dict)
            and response.get("success")
            and "backtest" in response
            and response["backtest"]
        ):
            backtest_data = response["backtest"]
            simplified_result = BacktestResult(
                status=backtest_data["status"],
                error=backtest_data["error"],
                hasInitializeError=backtest_data["hasInitializeError"],
            )

            # Return the simplified response
            return BacktestResponse(
                backtest=simplified_result,
                success=response["success"],
                errors=response.get("errors", []),
            )

        # If API call failed or no backtest data, return actual errors from API
        api_errors = []
        if isinstance(response, dict):
            # Extract errors from API response if available
            api_errors = response.get("errors", [])
            if not api_errors and not response.get("success"):
                api_errors = ["API call failed but no specific error provided"]

        if not api_errors:
            api_errors = ["No backtest data available"]

        return BacktestResponse(backtest=None, success=False, errors=api_errors)

    # 8. read_backtest_statistics (from tools/backtests.py)
    @mcp.tool(annotations={"title": "Read backtest statistics", "readOnlyHint": True})
    async def read_backtest_statistics(model: ReadBacktestRequest) -> BacktestResponse:
        """Read key performance statistics from backtest results."""
        response = await post("/backtests/read", model)

        # Create a simplified response with only the key statistics
        # The API response is a dict, not an object with attributes
        # Must check success=True before proceeding
        if (
            isinstance(response, dict)
            and response.get("success")
            and "backtest" in response
            and response["backtest"]
        ):
            backtest_data = response["backtest"]

            # Build simplified result with key statistics only
            simplified_result = BacktestResult(
                # Basic identification and status
                backtestId=backtest_data.get("backtestId"),
                status=backtest_data.get("status"),
                completed=backtest_data.get("completed"),
                error=backtest_data.get("error"),
                # Time information
                backtestStart=backtest_data.get("backtestStart"),
                backtestEnd=backtest_data.get("backtestEnd"),
                tradeableDates=backtest_data.get("tradeableDates"),
            )

            # Extract statistics if available - let Pydantic handle the field aliases
            if "statistics" in backtest_data and backtest_data["statistics"]:
                stats = backtest_data["statistics"]
                # Pass the statistics data directly to StatisticsResult
                # Pydantic will automatically map aliases like "Total Orders" to Total_Orders
                simplified_result.statistics = StatisticsResult(**stats)

            # Return the simplified response
            return BacktestResponse(
                backtest=simplified_result,
                success=response["success"],
                errors=response.get("errors", []),
            )

        # If API call failed or no backtest data, return actual errors from API
        api_errors = []
        if isinstance(response, dict):
            # Extract errors from API response if available
            api_errors = response.get("errors", [])
            if not api_errors and not response.get("success"):
                api_errors = ["API call failed but no specific error provided"]

        if not api_errors:
            api_errors = ["No backtest data available"]

        return BacktestResponse(backtest=None, success=False, errors=api_errors)

    # 9. search_quantconnect (from tools/ai.py)
    @mcp.tool(annotations={'title': 'Search QuantConnect', 'readOnlyHint': True})
    async def search_quantconnect(model: SearchRequest) -> SearchResponse:
        """Search for content in QuantConnect."""
        return await post('/ai/tools/search', model)

    logger.info("✅ Registered 9 essential tools for minimal server")


# Register the minimal tools
register_minimal_tools(mcp)

logger.info("✅ Tool registration process completed successfully")
logger.info(
    "🔒 Security: Only 9 essential tools exposed (87% reduction from full server)"
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
