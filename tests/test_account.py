import pytest
from json import loads

from main import mcp
from models import AccountResponse


class TestAccount:

    @pytest.mark.asyncio
    async def test_read_account(self):
        result = await mcp.call_tool('read_account', {})
        result = loads(result[0].text)
        assert result['success'], result
        assert AccountResponse.model_validate(result), 'Failed Pydantic conversion'
