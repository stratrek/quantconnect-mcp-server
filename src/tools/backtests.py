from api_connection import post
from models import (
    CreateBacktestRequest,
    ReadBacktestRequest,
    ReadBacktestChartRequest,
    ReadBacktestOrdersRequest,
    ReadBacktestInsightsRequest,
    ListBacktestRequest,
    UpdateBacktestRequest,
    DeleteBacktestRequest,
    BacktestResponse,
    BacktestResult,
    # LoadingChartResponse,
    ReadChartResponse,
    BacktestOrdersResponse,
    BacktestInsightsResponse,
    BacktestSummaryResponse,
    RestResponse,
    StatisticsResult,
    AlgorithmPerformance,
    PortfolioStatistics,
)


def register_backtest_tools(mcp):
    # Create
    @mcp.tool(annotations={"title": "Create backtest", "destructiveHint": False})
    async def create_backtest(model: CreateBacktestRequest) -> BacktestResponse:
        """Create a new backtest request and get the backtest Id."""
        return await post("/backtests/create", model)

    # Create a brief version that only returns essential fields
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

    # Read statistics for a single backtest.
    @mcp.tool(annotations={"title": "Read backtest", "readOnlyHint": True})
    async def read_backtest(model: ReadBacktestRequest) -> BacktestResponse:
        """Read the results of a backtest."""
        return await post("/backtests/read", model)

    # Read brief status for a single backtest.
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

    # Read key statistics for a single backtest.
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

            # Skip totalPerformance for now to isolate the issue
            # TODO: Re-enable after fixing validation issues
            # Extract key performance metrics if available
            # if (
            #     "totalPerformance" in backtest_data
            #     and backtest_data["totalPerformance"]
            # ):
            #     perf = backtest_data["totalPerformance"]
            #     key_perf = {}

            #     # Extract portfolio statistics if available
            #     if "portfolioStatistics" in perf and perf["portfolioStatistics"]:
            #         portfolio = perf["portfolioStatistics"]
                    
            #         def safe_float(value):
            #             """Convert string numbers to floats, return None for invalid values"""
            #             if value is None:
            #                 return None
            #             try:
            #                 return float(value)
            #             except (ValueError, TypeError):
            #                 return None
                    
            #         portfolio_stats = PortfolioStatistics(
            #             startEquity=safe_float(portfolio.get("startEquity")),
            #             endEquity=safe_float(portfolio.get("endEquity")),
            #             totalNetProfit=safe_float(portfolio.get("totalNetProfit")),
            #             sharpeRatio=safe_float(portfolio.get("sharpeRatio")),
            #             drawdown=safe_float(portfolio.get("drawdown")),
            #             compoundingAnnualReturn=safe_float(portfolio.get(
            #                 "compoundingAnnualReturn"
            #             )),
            #             winRate=safe_float(portfolio.get("winRate")),
            #             profitLossRatio=safe_float(portfolio.get("profitLossRatio")),
            #             expectancy=safe_float(portfolio.get("expectancy")),
            #             totalFees=safe_float(portfolio.get("totalFees")),
            #         )
                    
            #         algorithm_perf = AlgorithmPerformance(
            #             portfolioStatistics=portfolio_stats
            #         )
                    
            #         simplified_result.totalPerformance = algorithm_perf

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

    # Read a summary of all the backtests.
    @mcp.tool(annotations={"title": "List backtests", "readOnlyHint": True})
    async def list_backtests(model: ListBacktestRequest) -> BacktestSummaryResponse:
        """List all the backtests for the project."""
        return await post("/backtests/list", model)

    # Read the chart of a single backtest.
    @mcp.tool(annotations={"title": "Read backtest chart", "readOnlyHint": True})
    async def read_backtest_chart(model: ReadBacktestChartRequest) -> ReadChartResponse:
        """Read a chart from a backtest."""
        return await post("/backtests/chart/read", model)

    # Read the orders of a single backtest.
    @mcp.tool(annotations={"title": "Read backtest orders", "readOnlyHint": True})
    async def read_backtest_orders(
        model: ReadBacktestOrdersRequest,
    ) -> BacktestOrdersResponse:
        """Read out the orders of a backtest."""
        return await post("/backtests/orders/read", model)

    # Read the insights of a single backtest.
    @mcp.tool(annotations={"title": "Read backtest insights", "readOnlyHint": True})
    async def read_backtest_insights(
        model: ReadBacktestInsightsRequest,
    ) -> BacktestInsightsResponse:
        """Read out the insights of a backtest."""
        return await post("/backtests/read/insights", model)

    ## Read the report of a single backtest.
    # @mcp.tool(
    #    annotations={'title': 'Read backtest report', 'readOnlyHint': True}
    # )
    # async def read_backtest_report(
    #        model: BacktestReportRequest
    #    ) -> BacktestReport | BacktestReportGeneratingResponse:
    #    """Read out the report of a backtest."""
    #    return await post('/backtests/read/report', model)

    # Update
    @mcp.tool(annotations={"title": "Update backtest", "idempotentHint": True})
    async def update_backtest(model: UpdateBacktestRequest) -> RestResponse:
        """Update the name or note of a backtest."""
        return await post("/backtests/update", model)

    # Delete
    @mcp.tool(annotations={"title": "Delete backtest", "idempotentHint": True})
    async def delete_backtest(model: DeleteBacktestRequest) -> RestResponse:
        """Delete a backtest from a project."""
        return await post("/backtests/delete", model)
