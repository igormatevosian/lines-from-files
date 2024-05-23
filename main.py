import sys
import json
import typing as tp
from collections import defaultdict
from pathlib import Path

from config_loader import ConfigLoader


def resolve_path(base_path: Path, path_str: str) -> Path:
    """
    Returns the absolute path. If the path is relative, it combines it with base_path.

    Args:
        base_path (Path): The base path to use for relative paths.
        path (str): The path to resolve.

    Returns:
        Path: The resolved absolute path.
    """
    path = Path(path_str)
    return path if path.is_absolute() else base_path / path


def get_files_by_config(conf: ConfigLoader, base_path: Path) -> list[Path]:
    """
    Returns a list of file paths based on the configuration.

    Args:
        conf (ConfigLoader): The configuration loader object containing mode and path.
        base_path (Path): The base path for resolving relative paths.

    Returns:
        List[Path]: List of resolved file paths.
    """
    files = []
    if conf.mode == 'dir':
        dir_path = resolve_path(base_path, conf.path[0])
        if not dir_path.is_dir():
            raise ValueError(f"Path {dir_path} is not a valid directory.")
        files = sorted([file for file in dir_path.iterdir() if file.is_file()])
    elif conf.mode == 'files':
        for file in sorted(conf.path):
            file_path = resolve_path(base_path, file)
            if not file_path.is_file():
                raise ValueError(f"Path {file_path} is not a valid file.")
            files.append(file_path)
    else:
        raise Exception(f"Invalid mode: {conf.mode}")
    return files


def get_lines_from_files(files: list[Path]) -> list[list[str]]:
    """
    Returns a list of lines from each file.

    Args:
        files (List[Path]): List of file paths.

    Returns:
        List[List[str]]: List of lists containing lines from each file.
    """
    data = []
    for file_path in files:
        with file_path.open('r') as file:
            data.append([line.strip() for line in file.readlines()])
    return data


def create_data_from_line(file_lines: list[list[str]]) -> dict[int, dict[int, str]]:
    """
    Returns data organized by lines from files.

    Args:
        file_lines (List[List[str]]): List of lists containing lines from each file.

    Returns:
        Dict[int, Dict[int, str]]: Dictionary where the key is the line number and the value is a dictionary of file index and line content.
    """
    max_length = max(len(file) for file in file_lines)
    data: dict[int, tp.Any] = {i: defaultdict(dict) for i in range(max_length)}

    for line_number in range(max_length):
        for index, file in enumerate(file_lines):
            data[line_number][index] = file[line_number] if line_number < len(
                file) else ''
    return data


def main() -> None:
    """
    Main function to read configuration, process files, and output the results to a JSON file.
    """
    if len(sys.argv) != 3:
        print("Usage: python script.py <config_file> <config_id>")
        return

    config_file = Path(sys.argv[1]).resolve()
    config_id = int(sys.argv[2])

    conf = ConfigLoader(str(config_file), config_id)
    files = get_files_by_config(conf, config_file.parent)
    files_lines = get_lines_from_files(files)
    output_data = {
        "configFile": str(conf.config_file),
        "configurationID": conf.config_id,
        "configurationData": {
            "mode": conf.mode,
            "path": conf.path
        },
        "out": create_data_from_line(files_lines)
    }

    with open("output.json", 'w') as outfile:
        json.dump(output_data, outfile, indent=4)

    print("Output written to output.json")


if __name__ == "__main__":
    main()
