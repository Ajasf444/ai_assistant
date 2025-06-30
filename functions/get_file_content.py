import os

from google.genai import types

from config import MAX_CHARS

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


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_path = abs_working_dir
    if file_path:
        rel_path = os.path.join(working_directory, file_path)
        abs_target_path = os.path.abspath(rel_path)
    if not abs_target_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_target_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1) != "":
                file_content_string += (
                    f'[...File "{file_path}" truncated at 10_000 characters]'
                )
            return file_content_string
    except Exception as e:
        return f"Error: {e}"
