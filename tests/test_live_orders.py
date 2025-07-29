import pytest
from time import sleep

from main import mcp
from test_project import Project
from test_files import Files
from test_live import Live
from utils import validate_models
from models import LiveOrdersResponse, LoadingResponse


# Static helpers for common operations:
class LiveOrders:

    @staticmethod
    async def read(project_id, end, **kwargs):
        return await validate_models(
            mcp, 'read_live_orders', 
            {'projectId': project_id, 'end': end} | kwargs,
            LiveOrdersResponse | LoadingResponse
        )

    @staticmethod
    async def wait_for_orders_to_load(project_id, end=1_000):
        attempts = 0
        while attempts < 6*10:  # 10 minutes
            attempts += 1
            response = await LiveOrders.read(project_id, end)
            if isinstance(response, LiveOrdersResponse):
                return response.orders
            sleep(10)
        assert False, "Orders didn't load in time."


TEST_CASES = [
    ('Py', 'live_orders.py'),
    #('C#', 'LiveOrders.cs')
]
# Test suite:
class TestLiveOrders:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language, algo', TEST_CASES)
    async def test_read_live_orders(self, language, algo):
        # Create and compile the project.
        project_id, compile_id = await Files.setup_project(language, algo)
        # Deploy the algorithm.
        await Live.create(
            project_id, compile_id, await Live.get_node_id(project_id)
        )
        await Live.wait_for_algorithm_to_start(project_id)
        # Try to read the orders.
        orders = await LiveOrders.wait_for_orders_to_load(project_id)
        assert orders
        for order in orders:
            order.symbol.id == 'BTCUSD 2XR'
        # Stop the algorithm and delete the project to clean up.
        await Live.stop(project_id)
        await Project.delete(project_id)
