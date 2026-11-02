from pathlib import Path
from datetime import datetime

def scan_directory(directory_path):
    """
    Scans the specified directory and returns a list of files with their details.

    Args:
        directory_path (str): The path to the directory to scan.

    Returns:
        list: A list of dictionaries containing file details.
    """
    directory = Path(directory_path)
    
    files = []
    
    if not directory.exists():
        raise FileNotFoundError(f"The directory {directory_path} does not exist.")
    
    if not directory.is_dir():
        raise NotADirectoryError(f"The path {directory_path} is not a directory.")
    
    for file_path in directory.rglob('*'):
        if file_path.is_file():
            try:
                file_info = file_path.stat()
                
                file_data = {
                    'name': file_path.name,
                    'path': str(file_path.resolve()),
                    'extension': file_path.suffix.lower(),
                    'size': file_info.st_size,
                    'last_modified': datetime.fromtimestamp(file_info.st_mtime)
                }
                files.append(file_data)
            except (PermissionError, OSError) as e:
                print(f"Error accessing file {file_path}: {e}")

    return files