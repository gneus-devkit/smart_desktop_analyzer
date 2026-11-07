import csv
import json
from pathlib import Path
from datetime import datetime

REPORT_DIRETORY = Path("reports")

def prepare_report_directory():
    """Create the reports directory if it doesn't exist."""
    REPORT_DIRETORY.mkdir(parents=True, exist_ok=True)
    
def make_json_serializable(data):
    """Convert datetime objects and nested data into JSON-compatble values."""
    
    if isinstance(data, datetime):
        return data.isoformat()
    
    if isinstance(data, Path):
        return str(data)
    
    if isinstance(data, dict):
        return {key: make_json_serializable(value) for key, value in data.items()}
    
    if isinstance(data, (list, tuple)):
        return [make_json_serializable(item) for item in data]

    return data

def export_json(results, age_results, duplicates, recommendations):
    """Export the analysis results to a JSON file."""
    
    prepare_report_directory()
    
    file_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    report_path = REPORT_DIRETORY / file_name
    
    report_data = {
        "generated_at": datetime.now().isoformat(),
        "analysis": results,
        "age_results": age_results,
        "duplicates": duplicates,
        "recommendations": recommendations
    }
    
    with report_path.open("w", encoding="utf-8") as json_file:
        json.dump(make_json_serializable(report_data), json_file, indent=4)
    
    print(f"JSON report saved to {report_path.resolve()}")
    
    return report_path

def export_csv(files):
    """Export the scanned file inventory as a CSV file."""
    
    prepare_report_directory()
    
    file_name = f"file_details_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    report_path = REPORT_DIRETORY / file_name
    
    field_names = [
        "name",
        "path",
        "extension",
        "size",
        "last_modified"
    ]
    
    with report_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names, extrasaction="ignore")
        writer.writeheader()
        for item in files:
            writer.writerow(make_json_serializable(item))
    
    print(f"CSV report saved to {report_path.resolve()}")
    
    return report_path

def export_recommendations_csv(recommendations):
    """Export storage recommendations as a CSV file."""
    
    prepare_report_directory()
    
    file_name = f"recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    report_path = REPORT_DIRETORY / file_name
    
    field_names = [
        "priority",
        "type",
        "message",
        "name",
        "path",
        "size"
    ]
    
    with report_path.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names, extrasaction="ignore")
        writer.writeheader()
        for item in recommendations:
            writer.writerow(make_json_serializable(item))
    
    print(f"Recommendations CSV report saved to {report_path.resolve()}")
    
    return report_path