import pytest
from json import loads
from pydantic import ValidationError

async def validate_models(
        mcp, tool_name, input_args={}, input_class=None, output_class=None):
    if input_class:
        # The following line ensures we can convert the input dict to 
        # the input Pydantic model. If required arguments are missing 
        # or arguments are invalid, it raises an exception.
        input_model = input_class.model_validate(input_args)
    else:
        input_model = {}
    result = await mcp.call_tool(tool_name, input_model)
    output_json = loads(result[0].text)
    assert output_json['success'], output_json
    return output_class.model_validate(output_json)

async def raises_validation_error(tool_name, args, cls):
    with pytest.raises(ValidationError) as error:
        cls.model_validate(args)
    assert error.type is ValidationError
