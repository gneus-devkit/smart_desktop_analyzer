# Smart Desktop Analyzer

from analyzer import analyze_files
from scanner import scan_directory


def format_bytes(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    
    for unit in units:
        if size < 1024 or unit == "TB":
            return f"{size:.2f} {unit}"
        size /= 1024

def main():
    directory = input("Enter directory to anaylze: ")
    

    
    try:
        print("\nScanning directory...\n")
        
        files = scan_directory(directory)
        
        results = analyze_files(files)
        
        print("=" * 50)
        print("SMART DESKTOP ANALYZER")
        print("=" * 50)
        
        print(f"Total files: {results["total_files"]}")
        print(
            f"Total Storage: "
            f"{format_bytes(results["total_size"])}"
        )
        print(
            f"Average file size: "
            f"{format_bytes(results["average_size"])}"
        )
        
        print("\nFILE CATEGORIES")
        print("-" * 50)
        
        for category, count in results["category_counts"].items():
            size = results["category_sizes"][category]
            
            print(
                f"{category}: {count} files "
                f"{format_bytes(size)}"
            )
            
        print("\nFILE EXTENSIONS\n")
        print("-" * 50)
        
        for extension, count in sorted(results["extension_counts"].items(), key=lambda item: item[1], reverse=True):
            print(f"{extension or "[No extension]"}: {count}")
            
        print("\nLARGEST FILES\n")
        print("-" * 50)
        
        for file in results["largest_files"]:
            print(
                f"{file["name"]} - "
                f"{format_bytes(file["size"])}"
            )
        
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Error: {e}")



if __name__ == "__main__":
    main()
        