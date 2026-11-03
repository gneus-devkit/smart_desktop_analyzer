import hashlib
from collections import defaultdict


def calculate_file_hash(file_path):
    """"Calculate a file's SHA-256 has using memory-efficent chunks"""
    
    sha256 = hashlib.sha256()
    
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha256.update(chunk)
                
        return sha256.hexdigest()
          
    except (PermissionError, OSError) as e:
        print(f"Could not hash: {file_path}\nError: {e}")
        return None
       
def find_duplicates(files):
    """Find files with identical contents."""
    
    size_groups = defaultdict(list)
    
    for file in files:
        size_groups[file["sizes"]].append(file)
        
        hash_groups = defaultdict(list)
        for matching_size_files in size_groups.values():
            
            if len(matching_size_files) < 2:
                continue
            
            for file in matching_size_files:
                
                file_hash = calculate_file_hash(file["path"])
                
                if file_hash:
                    hash_groups[file_hash].append(file)
    duplicates = {
        file_hash: matching_files
        for file_hash, matching_files in hash_groups.items()
        if len(matching_files) > 1
    }
    
    return duplicates