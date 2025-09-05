from api_connection import post
from models import (
    CreateBacktestRequest,
    ReadBacktestRequest,
    ReadBacktestChartRequest,
    ReadBacktestOrdersRequest,
    ReadBacktestInsightsRequest,
    BacktestReportRequest,
    ListBacktestRequest,
    UpdateBacktestRequest,
    DeleteBacktestRequest,
    BacktestResponse,
    #LoadingChartResponse,
    ReadChartResponse,
    BacktestOrdersResponse,
    BacktestInsightsResponse,
    BacktestSummaryResponse,
    BacktestReport,
    BacktestReportGeneratingResponse,
    RestResponse
)

def register_backtest_tools(mcp):
    # Create
    @mcp.tool(
        annotations={
            'title': 'Create backtest',
            'destructiveHint': False
        }
    )
    async def create_backtest(
            model: CreateBacktestRequest) -> BacktestResponse:
        """Create a new backtest request and get the backtest Id."""
        return await post('/backtests/create', model)

    # Read statistics for a single backtest.
    @mcp.tool(annotations={'title': 'Read backtest', 'readOnlyHint': True})
    async def read_backtest(model: ReadBacktestRequest) -> BacktestResponse:
        """Read the results of a backtest."""
        return await post('/backtests/read', model)

    # Read brief status for a single backtest.
    @mcp.tool(annotations={'title': 'Read backtest brief', 'readOnlyHint': True})
    async def backtest_result_brief(model: ReadBacktestRequest) -> BacktestResponse:
        """Read a brief summary of backtest results containing only status, error, and hasInitializeError."""
        response = await post('/backtests/read', model)
        
        # Log the response for debugging
        import logging
        logger = logging.getLogger('quantconnect-mcp')
        logger.info(f"🔍 Backtest read API response type: {type(response)}")
        logger.info(f"🔍 Backtest read API response attributes: {dir(response)}")
        logger.info(f"🔍 Backtest read API response content: {response}")
        
        # Create a simplified response with only the required fields
        if hasattr(response, 'backtest') and response.backtest:
            from models import BacktestResult
            simplified_result = BacktestResult(
                status=response.backtest.status,
                error=response.backtest.error,
                hasInitializeError=response.backtest.hasInitializeError
            )
            
            # Return the simplified response
            from models import BacktestResponse
            return BacktestResponse(
                backtest=simplified_result,
                success=response.success,
                errors=response.errors
            )
        
        # If no backtest data, return minimal response (no fallback to full response)
        from models import BacktestResponse
        return BacktestResponse(
            backtest=None,
            success=False,
            errors=["No backtest data available"]
        )

    # Read a summary of all the backtests.
    @mcp.tool(annotations={'title': 'List backtests', 'readOnlyHint': True})
    async def list_backtests(
            model: ListBacktestRequest) -> BacktestSummaryResponse:
        """List all the backtests for the project."""
        return await post('/backtests/list', model)

    # Read the chart of a single backtest.
    @mcp.tool(
        annotations={'title': 'Read backtest chart', 'readOnlyHint': True}
    )
    async def read_backtest_chart(
            model: ReadBacktestChartRequest) -> ReadChartResponse:
        """Read a chart from a backtest."""
        return await post('/backtests/chart/read', model)
    
    # Read the orders of a single backtest.
    @mcp.tool(
        annotations={'title': 'Read backtest orders', 'readOnlyHint': True}
    )
    async def read_backtest_orders(
            model: ReadBacktestOrdersRequest) -> BacktestOrdersResponse:
        """Read out the orders of a backtest."""
        return await post('/backtests/orders/read', model)
    
    # Read the insights of a single backtest.
    @mcp.tool(
        annotations={'title': 'Read backtest insights', 'readOnlyHint': True}
    )
    async def read_backtest_insights(
            model: ReadBacktestInsightsRequest) -> BacktestInsightsResponse:
        """Read out the insights of a backtest."""
        return await post('/backtests/read/insights', model)
    
    ## Read the report of a single backtest.
    #@mcp.tool(
    #    annotations={'title': 'Read backtest report', 'readOnlyHint': True}
    #)
    #async def read_backtest_report(
    #        model: BacktestReportRequest
    #    ) -> BacktestReport | BacktestReportGeneratingResponse:
    #    """Read out the report of a backtest."""
    #    return await post('/backtests/read/report', model)

    # Update
    @mcp.tool(
        annotations={'title': 'Update backtest', 'idempotentHint': True}
    )
    async def update_backtest(model: UpdateBacktestRequest) -> RestResponse:
        """Update the name or note of a backtest."""
        return await post('/backtests/update', model)
    
    # Delete
    @mcp.tool(
        annotations={'title': 'Delete backtest', 'idempotentHint': True}
    )
    async def delete_backtest(model: DeleteBacktestRequest) -> RestResponse:
        """Delete a backtest from a project."""
        return await post('/backtests/delete', model)
