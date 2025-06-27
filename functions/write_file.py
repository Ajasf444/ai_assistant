import os


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_path = abs_working_dir
    if file_path:
        rel_path = os.path.join(working_directory, file_path)
        abs_target_path = os.path.abspath(rel_path)
    else:
        return f"Error: No file path provided."
    if not abs_target_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_target_path):
        os.makedirs(os.path.dirname(abs_target_path), exist_ok=True)
    with open(abs_target_path, "w") as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


if __name__ == "__main__":
    pass
