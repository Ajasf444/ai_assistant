import os

from google.genai import types

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


def get_files_info(working_directory, directory=None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_path = abs_working_dir
    if directory:
        rel_path = os.path.join(working_directory, directory)
        abs_target_path = os.path.abspath(rel_path)
    if not abs_target_path.startswith(abs_working_dir):
        print(abs_target_path)
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(abs_target_path):
        return f'Error: "{directory}" is not a directory'
    try:
        return _get_formatted_info(abs_target_path)
    except Exception as e:
        return f"Error: {e}"


def _get_formatted_info(path):
    items = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        items.append(_get_formatted_item(item_path, item))
    return "\n".join(items)


def _get_formatted_item(path, item):
    size = os.path.getsize(path)
    is_dir = os.path.isdir(path)
    return f"- {item}: file_size={size} bytes, is_dir={is_dir}"
