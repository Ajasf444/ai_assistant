from google.genai import types

from config import WORKING_DIRECTORY
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

FUNCTIONS = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)


def call_function(function_call_part: types.FunctionCall, verbose=False):
    func = function_call_part.name
    if func not in FUNCTIONS:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func,
                    response={"error": f"Unknown function: {func}"},
                )
            ],
        )
    args = {"working_directory": WORKING_DIRECTORY}
    args.update(function_call_part.args)
    if verbose:
        print(f"Calling function: {func}({args})")
    else:
        print(f" - Calling function: {func}")
    result = FUNCTIONS[func](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func,
                response={"result": result},
            )
        ],
    )
