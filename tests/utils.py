import pytest
import jsonschema
from json import loads
from pydantic import ValidationError

async def validate_models(mcp, tool_name, input_args={}, output_class=None):
    # Run the tool. If the input args are invalid, it raises an error.
    result = await mcp.call_tool(tool_name, input_args) # a tuple
    text_contents = result[0] # A list of TextContent objects
    structured_response = result[1]
    # Check if the response has the success flag.
    assert loads(text_contents[0].text)['success'], 'Request failed'    
    # Check if the response schema is valid JSON.
    jsonschema.validate(
        instance=structured_response, 
        schema=mcp._tool_manager.get_tool(tool_name).fn_metadata.output_schema
    )
    # Create and return the output model.
    return output_class.model_validate(structured_response)

async def raises_validation_error(tool_name, args, cls):
    with pytest.raises(ValidationError) as error:
        cls.model_validate(args)
    assert error.type is ValidationError
