import pytest
import jsonschema
from json import loads
from pydantic import ValidationError
from datetime import datetime

async def validate_models(
        mcp, tool_name, input_args={}, output_class=None, 
        success_expected=True):
    # Call the tool with the arguments. If the input args are invalid,
    # it raises an error.
    unstructured_response, structured_response = await mcp.call_tool(
        tool_name, {'model': input_args} if input_args else {}
    )
    # Check if the response has the success flag.
    assert loads(unstructured_response[0].text)['success'] == success_expected,\
        structured_response
    if not success_expected:
        return
    # Check if the response schema is valid JSON.
    jsonschema.validate(
        instance=structured_response, 
        schema=mcp._tool_manager.get_tool(tool_name).fn_metadata.output_schema
    )
    # Create and return the output model.
    return output_class.model_validate(structured_response)

async def raises_validation_error(tool_name, args, class_):
    with pytest.raises(ValidationError) as error:
        class_.model_validate(args)
    assert error.type is ValidationError

async def send_request_with_invalid_args(
        mcp, tool_name, class_, payload, invalid_arguments):
    # Try to send the request without providing all the required 
    # arguments.
    for key in payload:
        await raises_validation_error(
            tool_name, 
            {k: v for k, v in payload.items() if k != key}, 
            class_
        )
    # Try to send the request with an invalid argument.
    for arg in invalid_arguments:
        await validate_models(
            mcp, tool_name, payload | arg, class_, False
        )

def create_timestamp():
    return datetime.now().strftime('%Y%m%d_%H%M%S_%f')
