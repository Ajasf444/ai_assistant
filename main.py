import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function
from system_prompt import system_prompt

api_key = os.environ.get("GEMINI_API_KEY")


def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv

    len_inputs = len(sys.argv)
    if len_inputs < 2:
        print("Error: No prompt supplied.")
        exit(1)

    client = genai.Client(api_key=api_key)
    args = [arg for arg in sys.argv if not arg.startswith("--")]
    user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Reads the content of a specified file up to 10_000 characters, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path to the file to read from, relative to the working directory. If no file exists returns an error text.",
                ),
            },
        ),
    )
    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Runs a Python file, i.e., one that ends with .py file extension, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path to the Python file to execute. If no file path is provided returns an error text.",
                ),
            },
        ),
    )
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes content to a file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path to the file to write to. If no file path is provided returns an error text.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to be written into the file.",
                ),
            },
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if response.function_calls:
        for function_call_part in response.function_calls:
            print(
                f"Calling function: {function_call_part.name}({
                    function_call_part.args
                })"
            )
            function_call_result = call_function(function_call_part, verbose)
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Function call error!")
    if verbose:
        # print(f"User prompt: {response.text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {
              response.usage_metadata.candidates_token_count}")
        print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
