import os
import subprocess

from google.genai import types

from config import PROCESS_TIMEOUT

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


def run_python_file(working_directory, file_path, args=None):
    abs_working_directory = os.path.abspath(working_directory)
    target_path = abs_working_directory
    if file_path:
        target_path = os.path.abspath(
            os.path.join(working_directory, file_path))
    else:
        return f"Error: No path to Python file provided."
    if not target_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'
    if not target_path.endswith(".py"):
        print(target_path)
        return f'Error: "{file_path}" is not a Python file.'
    try:
        commands = ["python3", target_path]
        if args:
            commands.extend(args)
        process_result = subprocess.run(
            args=commands,
            cwd=abs_working_directory,
            timeout=PROCESS_TIMEOUT,
            capture_output=True,
            text=True,
        )
        output = []
        if process_result.stdout:
            output.append(f"STDOUT:\n{process_result.stdout}")
        if process_result.stderr:
            output.append(f"STDERR:\n{process_result.stderr}")
        if process_result.returncode != 0:
            output += f"Process excited with code {process_result.returncode}"
        return "\n".join(output) if output else "No output produced."

    except Exception as e:
        return f"Error: executing Python file: {e}"


if __name__ == "__main__":
    result = run_python_file("calculator", "nonexistent.py")
    print(result)
