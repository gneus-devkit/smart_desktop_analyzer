from pathlib import Path
from datetime import datetime
from tqdm import tqdm

def scan_directory(directory_path):
    """
    Scans the specified root_directory and returns a list of files with their details.
    
    Displays a progress bar showing scan completion.
    Files are only read for metadata; they are never modified.
    
    Args:
        directory_path (str): The path to the root_directory to scan.

    Returns:
        list: A list of dictionaries containing file details.
    """
    root_directory = Path(directory_path)
    
    files = []
    
    if not root_directory.exists():
        raise FileNotFoundError(f"The directory {directory_path} does not exist.")
    
    if not root_directory.is_dir():
        raise NotADirectoryError(f"The path {directory_path} is not a directory.")
    
    print("\nPreparing directory scan...")
    
    # 1st scan to count number of files.
    total_files = sum(
        1
        for path in root_directory.rglob("*")
        if path.is_file()
    )
    
    print(f"Found {total_files:,} files to scan.\n")
    
    # 2nd scan to track progress of scan
    files = []
    
    file_iterator = (
        path
        for path in root_directory.rglob("*")
        if path.is_file()
    )
    
    with tqdm(
        total=total_files,
        desc="Scanning files",
        unit="file",
        dynamic_ncols=True,
        mininterval=0.2,
    ) as progress:
        
        for file_path in file_iterator:
            
            try:
                file_stats = file_path.stat()
                
                file_info = {
                    "name": file_path.name,
                    "path": str(file_path),
                    "extension": file_path.suffix.lower(),
                    "size": file_stats.st_size,
                    "last_modified": datetime.fromtimestamp(file_stats.st_mtime),                    
                }
                
                files.append(file_info)
                
            except (PermissionError, OSError):
                pass
                
            finally:
                progress.update(1)

    return files