import pytest
import jsonschema
from json import loads
from pydantic import ValidationError
from datetime import datetime

async def validate_models(mcp, tool_name, input_args={}, output_class=None):
    # Call the tool with the arguments. If the input args are invalid,
    # it raises an error.
    unstructured_response, structured_response = await mcp.call_tool(
        tool_name, {'model': input_args} if input_args else {}
    )
    # Check if the response has the success flag.
    assert loads(unstructured_response[0].text)['success'], structured_response
    # Check if the response schema is valid JSON.
    jsonschema.validate(
        instance=structured_response, 
        schema=mcp._tool_manager.get_tool(tool_name).fn_metadata.output_schema
    )
    # Create and return the output model.
    return output_class.model_validate(structured_response)

async def raises_validation_error(tool_name, args, cls):
    with pytest.raises(ValidationError) as error:
        cls.model_validate({'model': args})
    assert error.type is ValidationError

def create_timestamp():
    return datetime.now().strftime('%Y%m%d_%H%M%S_%f')
