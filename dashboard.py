from pathlib import Path

from scanner import scan_directory
from analyzer import analyze_files, analyze_directory_usage
from duplicate_finder import find_duplicates
from age_analyzer import analyze_file_age
from recommendations import generate_recommendations
from reporter import (
    export_json,
    export_csv,
    export_recommendations_csv,
)

def format_bytes(size):
    """Convert bytes into a readable storage size."""

    units = ["B", "KB", "MB", "GB", "TB"]
    
    for unit in units:
        if size < 1024 or unit == "TB":
            return f"{size:.2f} {unit}"
        
        size /= 1024
        
def pause():
    """Wait for the user before returning to the menu"""
    
    input("\nPress Enter to return to the menu...")
    
def display_menu():
    """Display the main application menu."""
    
    print("\n" + ("=" * 55))
    print("SMART DESKTOP ANALYZER".center(55))
    print("=" * 55)
    
    options = {
        "1": "Scan a directory",
        "2": "View storage overview",
        "3": "View file categories",
        "4": "Find largest files",
        "5": "Find duplicate files",
        "6": "View file age analysis",
        "7": "View storage recommendations",
        "8": "Export records",
        "9": "Change scan directory",
        "10": "View directory storage analysis",
        "0": "Exit"
    }
    
    for key, description in options.items():
        print(f"    {key}. {description}")
        
    print("=" * 55)
    
    choice = input("\nSelect an option (0-10): ").strip()
    
    if not choice:
        print("\nNo selection entered. Please enter a number.")
        return None
    
    return choice
    
def run_scan(directory):
    """Run all analytics modules return their results."""
    
    print("\nStarting directory scan...")
    print(f"Directory: {directory}")
    print("-" * 55)
    
    files = scan_directory(str(directory))
    
    print(f"Files discovered: {len(files)}")
    print("Analyzing files...")
    
    results = analyze_files(files)
    directory_usage = analyze_directory_usage(files, directory)
    
    print(("Checking for duplicates..."))
    duplicates = find_duplicates(files)
    
    print("Analyzing file ages...")
    age_results = analyze_file_age(files)
    
    print("Generating recommendations...")
    recommendations = generate_recommendations(files, duplicates)
    
    print("\nScan completed sucessfully.")
    
    return {
        "files": files,
        "results": results,
        "duplicates": duplicates,
        "age_results": age_results,
        "recommendations": recommendations,
        "directory_usage": directory_usage,
    }
    
def display_storage_overview(data):
    """Displays the general storage overview."""
    
    results = data["results"]
    
    print("\n" + ("=" * 55))
    print("STORAGE OVERVIEW".center(55))
    print("=" * 55)
    
    print(f"Total files:        {results["total_files"]:,}")
    print(f"Total storage:      {format_bytes(results["total_size"])}")
    print(f"Average file size:  {format_bytes(results["average_size"])}")
    
    print("=" * 55)
    
def display_categories(data):
    """Displays file categories and their storage usage."""
    
    results = data["results"]
    
    print("\n" + ("=" * 55))
    print("FILE CATEGORIES".center(55))
    print("=" * 55)
    print(
        f"{"Category":<20}"
        f"{"Files":>12}"
        f"{"Storage":>18}"
    )
    
    for category, count in sorted(results["category_counts"].items()):
        size = results["category_sizes"].get(category, 0)
        
        print(
            f"{category:<20} "
            f"{count:>12,} files    "
            f"{format_bytes(size):>19}"
        )
        
    print("\n" + ("=" * 55))
    print("STORAGE BREAKDOWN BY EXTENSION".center(55)) 
    print("=" * 55)
    
    print(
        f"{"Extension":<20}"
        f"{"Files":>12}"
        f"{"Storage":>18}"
    )
    
    print("-" * 55)
    
    extension_counts = results["extension_counts"]
    extension_sizes = results["extension_sizes"]
    
    sorted_extensions = sorted(extension_sizes.items(), key=lambda item: item[1], reverse=True)
    
    for extension, size in sorted_extensions:
        count = extension_counts.get(extension, 0)
        
        display_extension = extension if extension else "[no extension]"
    
        print(
            f"{display_extension:<20}"
            f"{count:>12,}"
            f"{format_bytes(size):>18}"
        )
    print("=" * 55)
    
def display_largest_files(data):
    """Displayus the largest files discovered during the scan"""
    
    largest_files = data["results"]["largest_files"]
    
    print("\n" + ("=" * 55))
    print("LARGEST FILES".center(55))
    print("=" * 55)
    
    if not largest_files:
        print("No files found.")
        return
    
    for index, file in enumerate(largest_files[:10], start=1):
        print(f"\n{index}. {file["name"]}")
        print(f"    Size: {format_bytes(file["size"])}")
        print(f"    Path: {file["path"]}")
        
def display_duplicates(data):
    """Display verified duplicate file groups."""
    
    duplicates = data["duplicates"]
    
    print("\n" + ("=" * 55))
    print("DUPLICATE FILES".center(55))
    print("=" * 55)
    
    if not duplicates:
        print("No duplicate files found.")
        return
    
    print(f"Duplicate groups: {len(duplicates)}")
    
    for index, (file_hash, files) in enumerate(duplicates.items(), start=1):
        print(f"\nGroup {index}")
        print(f"Matching files: {len(files)}")
        
    for file in files:
        print(f"    - {file["path"]}")
    
    print(f"    File size: {format_bytes(files[00]["size"])}")
    
def display_file_age(data):
    "Display file age statistics."
    
    age_results = data["age_results"]
    
    print("\n" + ("=" * 55))
    print("FILE AGE ANALYSIS".center(55))
    print("=" * 55)
    
    for age_range, count in age_results["age_counts"].items():
        print(f"{age_range:<25} {count:>8} files")
        
    print("=" * 55)
        
    print((
        "Files at least 180 days old: "
        f"{age_results["old_file_count"]}"
    ))
        
    print(
        "Large old files (100 MB+): "
        f"{len(age_results["large_old_files"]):,}"
    )
        
    print("\nOLDEST FILES")
    print("=" * 55)
        
    for index, file in enumerate(age_results["oldest_files"][:10], start=1):
        print(f"{index}. {file["name"]}")
        print(f"    Last modified: {file["last_modified"]}")
        print(f"    Size: {format_bytes(file["size"])}")
        
def display_recommendations(data):
    """Displays storage recommendations."""
    
    recommendations = data["recommendations"]
    
    print("\n" + ("=" * 55))
    print("STORAGE RECOMMENDATIONS".center(55))
    print("=" * 55)
    
    if not recommendations:
        print("No storage recommendations at this time.")
        return
    
    priority_order = ["High", "Medium", "Low"]
    
    for priority in priority_order:
        matching = [item for item in recommendations if item["priority"] == priority]
        
        if not matching:
            continue
        
    print(f"\n{priority.upper()} PRIORITY")
    print("=" * 55)
    
    for item in matching:
        print(f"\nType: {item["type"]}")
        print(f"File: {item["name"]}")
        print(f"Size: {format_bytes(item["size"])}")
        print(f"Details: {item["message"]}")
        print(f"Path: {item["path"]}")
        
def display_directory_usage(data):
    """Display storage usage by top-level directory."""

    directory_usage = data[["directory_usage"]]
    total_size = data["results"]["total_size"]
    
    print("\n" + ("=" * 70))
    
    print("DIRCTORY STORAGE ANALYSIS".center(70))
    
    if not directory_usage:
        print(
            f"{"Directory":<30}"
            f"{"Files":>12}"
            f"{"Storage":>16}"
            f"{"Share":>10}"
        )
        
        print("-" * 70)
        
    for item in directory_usage:
        size = item["total_size"]
        
        percentage = (
            size / total_size * 100
            if total_size
            else 0
        )
        
        print(
            f"{item["directory"][:29]:<30}"
            f"{item["file_count"]:>12,}"
            f"{format_bytes(size):>16}"
            f"{percentage:>9.1f}%"
        )
        
    print("=" * 70)
    print(
        f"Showing {len(directory_usage)} largest "
        "top-kevek directories"
    )
        
def export_reports(data):
    """Export JSON and CSV reports."""
    
    print("\nGenerating reports...")
    
    json_report = export_json(data["results"], data["age_results"], data["duplicates"], data["recommendations"],)
    
    inventory_report = export_csv(data["files"])
    
    recommendations_report = export_recommendations_csv(data["recommendations"])
    
    print("\n" + ("=" * 55))
    print("REPORTS GENERATED".center(55))
    print("=" * 55)
    
    print(f"JSON report:            {json_report}")
    print(f"Inventory CSV:          {inventory_report}")
    print(f"Recommendations CSV:    {recommendations_report}")
    
def run_dashboard():
    """Run the interactive application dashboard."""
    
    directory = None
    data = None
    
    while True:
        choice = display_menu()
        
        try:
            if choice == "1":
                
                if directory is None:
                    directory_input = input("\nEnter Directory to scan: ").strip()
                    
                    directory = Path(directory_input).expanduser()
                    
                if not directory.is_dir():
                    print("\nInvalid directory. Please try again.")
                    directory = None
                    pause()
                    continue
                
                data = run_scan(directory.resolve())
                pause()
                
            elif choice == "2":
                
                if data is None:
                    print("\nPlease scan a directory first.")
                else:
                    display_storage_overview(data)
                    
                pause()
                
            elif choice == "3":
                
                if data is None:
                    print("\nPlease scan a directory first.")
                else:
                    display_categories(data)
                    
                pause()
                
            elif choice == "4":
                
                if data == None:
                    print("\nPlease scan a directory first.")
                else:
                    display_largest_files(data)
                    
                pause()
                
            elif choice == "5":
                
                if data == None:
                    print("\nPlease scan a directory first.")
                else:
                    display_duplicates(data)
                    
                pause()
                
            elif choice == "6":
                
                if data == None:
                    print("\nPlease scan a directory first.")
                else:
                    display_file_age(data)
                    
                pause()
                
            elif choice == "7":
                
                if data == None:
                    print("\nPlease scan a directory first.")
                else:
                    display_recommendations(data)
                    
                pause()
                
            elif choice == "8":
                
                if data == None:
                    print("\nPlease scan a directory first.")
                else:
                    export_reports(data)
                    
                pause()
                
            elif choice == "9":
                
                new_directory = input("\nEnter the new directory path: ").strip()
                new_directory = Path(new_directory).expanduser()
                
                if new_directory.is_dir():
                    directory = new_directory.resolve()
                    data = None
                    
                    print("\nDirectory changed successfully.")
                    print("Run option 1 to scan the new directory.")
                    
                else:
                    print("\nInvalid directory. Directory was not changed.")
                    
                pause()
                
            elif choice == "10":
                
                if data == None:
                    print("\nPlease scan a directory first.")
                else:
                    display_directory_usage(data)
                
                pause()
                
            elif choice == "0":
                
                print("\nThank you for using Smart Desktop Analyzer.")
                break
            
            else:
                
                print("\nInvalid selection. Please try again.")
                
        except (PermissionError, OSError) as e:
            print(f"\nFile system error: {e}")
            pause()
            
        except Exception as e:
            print(f"An unexpected error has occurred: {e}")
            pause()
            
            
if __name__ == "__main__":
    run_dashboard()