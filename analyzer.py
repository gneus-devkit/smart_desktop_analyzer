from pathlib import Path

FILE_CATEGORIES = {
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"
    ],
    "Documents": [
        ".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xlsx", ".csv", ".ppt", ".pptx"
    ],
    "Videos": [
        ".mp4", ".mov", ".avi", ".mkv", ".wmv", ".webm"
    ],
    "Audio": [
        ".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"
    ],
    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz"
    ],
    "Executables": [
        ".exe", ".msi", ".bat", ".cmd", ".ps1"
    ],
    "Code": [
        ".py", ".js", ".jsx", ".html", ".php", ".cpp", ".go", ".css", ".c", ".java", ".json", ".sql", ".ts", ".tsx"
    ]
}

def categorize_files(extension):
    for category, extensions in FILE_CATEGORIES.items():
        if extension.lower() in extensions:
            return category
        
    return "Other"
        
def analyze_files(files):
    total_size = 0
    
    extension_counts = {}
    extension_sizes = {}
    
    category_counts = {}
    category_sizes = {}
    
    for file in files:
        extension = file["extension"].lower()
        size = file["size"]
        
        total_size += size
        
        extension_counts[extension] = extension_counts.get(extension, 0) + 1
        extension_sizes[extension] = extension_sizes.get(extension, 0) + size
        
        category = categorize_files(extension)
        
        category_counts[category] = category_counts.get(category, 0) + 1
        category_sizes[category] = category_sizes.get(category, 0) + size
        
    largest_files = sorted(files, key=lambda file: file["size"], reverse=True)[:10]
        
    smallest_files = sorted(files, key=lambda file: file["size"])[:10]
        
    average_size = total_size/len(files) if files else 0
        
    return {
        "total_files": len(files),
        "total_size": total_size,
        "average_size": average_size,
        "extension_counts": extension_counts,
        "extension_sizes": extension_sizes,
        "category_counts": category_counts,
        "category_sizes": category_sizes,
        "largest_files": largest_files,
        "smallest_files": smallest_files
    }
    
def analyze_directory_usage(files, root_directory, limit=20):
    """Aggregate file storage by top-level directory"""
    
    root = Path(root_directory).resolve()
    directory_stats = {}
    
    for file in files:
        file_path = Path(file["path"])
        
        try:
            relative_path = file_path.relative_to(root)
        except ValueError:
            continue
        
        if len(relative_path.parts) == 1:
            directory_name = "[root]"
        else:
            directory_name = relative_path.parts[0]
            
        if directory_name not in directory_stats:
            directory_stats[directory_name] = {
                "file_count": 0,
                "total_size": 0,
            }
            
        directory_stats[directory_name]["file_count"] += 1
        directory_stats[directory_name]["total_size"] += file["size"]
        
    ranked_directories = sorted(
        directory_stats.items(),
        key=lambda item: item[1]["total_size"],
        reverse=True,
    )
    
    return [
        {
            "directory": name,
            "file_count": stats["file_count"],
            "total_size": stats["total_size"],
        }
        for name, stats in ranked_directories[:limit]
    ]