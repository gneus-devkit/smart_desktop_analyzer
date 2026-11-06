# Smart Desktop Analyzer

from age_analyzer import analyze_file_age
from analyzer import analyze_files
from duplicate_finder import find_duplicates
from recommendations import generate_recommendations
from reporter import export_json, export_csv, export_recommendations_csv
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
        
        age_results = analyze_file_age(files)
        
        duplicates = find_duplicates(files)
        
        recommendations = generate_recommendations(files, duplicates)
        
        duplicate_groups = len(duplicates)
        
        duplicate_file_count = sum(
            len(group) for group in duplicates.values()
        )
        
        redundant_file_count = sum(
            len(group) - 1 for group in duplicates.values()
        )
        
        duplicate_storage = sum(
            (len(group) - 1) * group[0]["size"]
            for group in duplicates.values()
        )
        
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
        
        print("\nDUPLICATE FILE ANALYSIS")
        print("-" * 50)

        print(f"Duplicate groups: {duplicate_groups}")
        print(f"Files involved: {duplicate_file_count}")
        print(f"Redundant copies: {redundant_file_count}")

        print(
            f"Potential storage savings: "
            f"{format_bytes(duplicate_storage)}"
        )

        if duplicates:
            print("\nDUPLICATE FILE GROUPS")
            print("-" * 50)

            for number, (file_hash, group) in enumerate(
                duplicates.items(), start=1
            ):
                print(f"\nGroup {number}")
                print(f"SHA-256: {file_hash}")

                for file in group:
                    print(f"  {file['name']}")
                    print(f"  Location: {file['path']}")

        else:
            print("\nNo duplicate files found.")
            
            
        
        print("\nFILE AGE ANALYSIS")
        print("-" * 50)

        for age_range, count in age_results["age_counts"].items():
            print(f"{age_range}: {count} files")

        print(
            f"\nFiles older than 180 days: "
            f"{age_results['old_file_count']}"
        )

        print("\nOLDEST FILES")
        print("-" * 50)

        for file in age_results["oldest_files"]:
            print(
                f"{file['name']} - "
                f"{file['age_days']} days old"
            )

        print("\nLARGE OLD FILES")
        print("-" * 50)

        if age_results["large_old_files"]:
            for file in age_results["large_old_files"]:
                print(
                    f"{file['name']} - "
                    f"{format_bytes(file['size'])} - "
                    f"{file['age_days']} days old"
                )
        else:
            print("No large old files found.")
            
        
        print("\nSTORAGE RECOMMENDATIONS")
        print("=" * 50)

        if recommendations:

            print(
                f"Total recommendations: {len(recommendations)}"
            )

            high_count = sum(
                1 for item in recommendations
                if item["priority"] == "High"
            )

            medium_count = sum(
                1 for item in recommendations
                if item["priority"] == "Medium"
            )

            low_count = sum(
                1 for item in recommendations
                if item["priority"] == "Low"
            )

            print(f"High priority: {high_count}")
            print(f"Medium priority: {medium_count}")
            print(f"Low priority: {low_count}")

            for number, item in enumerate(
                recommendations, start=1
            ):
                print("\n" + "-" * 50)

                print(
                    f"Recommendation #{number} "
                    f"[{item['priority']}]"
                )

                print(f"Type: {item['type']}")
                print(f"File: {item['name']}")
                print(f"Reason: {item['message']}")
                print(f"Size: {format_bytes(item['size'])}")
                print(f"Location: {item['path']}")

        else:
            print("No storage recommendations at this time")
            
            json_report = export_json(
            results,
            age_results,
            duplicates,
            recommendations
        )

        inventory_report = export_csv(files)

        recommendations_report = export_recommendations_csv(
            recommendations
        )

        print("\nREPORTS GENERATED")
        print("-" * 50)

        print(f"JSON report: {json_report}")
        print(f"Inventory CSV: {inventory_report}")
        print(f"Recommendations CSV: {recommendations_report}")
            
        
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"Error: {e}")



if __name__ == "__main__":
    main()
        