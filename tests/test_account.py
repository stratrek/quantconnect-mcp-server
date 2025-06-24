import pytest
from json import loads

from main import mcp
from models import AccountResponse

import os

class TestAccount:

    @pytest.mark.asyncio
    async def test_read_account(self):
        result = await mcp.call_tool('read_account', {})
        assert result.success, str(result)
        assert AccountResponse.model_validate(loads(result[0].text))
