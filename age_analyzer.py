from datetime import datetime


def analyze_file_age(files):
    """Analyze files age using their last modified timestamps"""
    
    now = datetime.now()
    
    age_counts = {
        "less than 30 days": 0,
        "30 to 89 days": 0,
        "90 to 179 days": 0,
        "180 to 364 days": 0,
        "365+ days": 0
    }
    
    old_files = []
    large_old_files = []
    
    for file in files:
        modified = file["last_modified"]
        age = (now - modified).days
        
        file_info = {
            **file,
            "age_days": age
        }
        
        if age < 30:
            age_counts["less than 30 days"] += 1
        if age < 90:
            age_counts["30 to 89 days"] += 1
        if age < 180:
            age_counts["90 to 179 days"] += 1
        if age < 360:
            age_counts["180 to 364 days"] += 1
        else:
            age_counts["365+ days"]
        
        if age <= 180:
            old_files.append(file_info)    
            
        if age <= 180 and file["size"] > 100 * 1024 * 1024:
            large_old_files.append(file_info)
            
    oldest_files = sorted(old_files, key=lambda file: file["age_days"], reverse=True)[:10]
    
    large_old_files.sort(key=lambda file: file["size"], reverse=True)
    
    return {
        "age_counts": age_counts,
        "old_file_count": len(old_files),
        "large_old_files": large_old_files,
        "oldest_files": oldest_files
    }
        