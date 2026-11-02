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
    category_counts = {}
    category_sizes = {}
    
    for file in files:
        extension = file["extension"].lower()
        size = file["size"]
        
        total_size += size
        
        extension_counts[extension] = extension_counts.get(extension, 0) + 1
        
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
        "category_counts": category_counts,
        "category_sizes": category_sizes,
        "largest_files": largest_files,
        "smallest_files": smallest_files
    }