from datetime import datetime

# Recommendation thresholds
LARGE_FILE_SIZE = 100 * 1024 * 1024       # 100 MB
VERY_LARGE_FILE_SIZE = 500 * 1024 * 1024  # 500 MB
OLD_FILE_DAYS = 365
VERY_OLD_FILE_DAYS = 730


def generate_recommendations(files, duplicates):
    """Generate storage recommendations without changing files."""

    recommendations = []

    now = datetime.now()

    # Analyze individual files
    for file in files:
        size = file["size"]
        modified = file["last_modified"]
        age_days = (now - modified).days

        # Very large files
        if size >= VERY_LARGE_FILE_SIZE:
            recommendations.append({
                "priority": "High",
                "type": "Very large file",
                "message": (
                    f"Review this file because it uses "
                    f"{size / (1024 ** 2):.2f} MB of storage."
                ),
                "name": file["name"],
                "path": file["path"],
                "size": size
            })

        # Large files
        elif size >= LARGE_FILE_SIZE:
            recommendations.append({
                "priority": "Medium",
                "type": "Large file",
                "message": "Review whether this large file is still needed.",
                "name": file["name"],
                "path": file["path"],
                "size": size
            })

        # Very old files
        if age_days >= VERY_OLD_FILE_DAYS:
            recommendations.append({
                "priority": "Medium",
                "type": "Very old file",
                "message": (
                    f"This file has not been modified "
                    f"for {age_days} days."
                ),
                "name": file["name"],
                "path": file["path"],
                "size": size
            })

        elif age_days >= OLD_FILE_DAYS:
            recommendations.append({
                "priority": "Low",
                "type": "Old file",
                "message": (
                    f"This file has not been modified "
                    f"for {age_days} days."
                ),
                "name": file["name"],
                "path": file["path"],
                "size": size
            })

    # Analyze duplicate groups
    for group in duplicates.values():

        if len(group) < 2:
            continue

        redundant_copies = len(group) - 1
        potential_savings = redundant_copies * group[0]["size"]

        recommendations.append({
            "priority": "High",
            "type": "Duplicate files",
            "message": (
                f"Found {len(group)} identical files. "
                f"Reviewing the extra copies could free "
                f"{potential_savings / (1024 ** 2):.2f} MB."
            ),
            "name": group[0]["name"],
            "path": group[0]["path"],
            "size": potential_savings
        })

    # Sort recommendations by priority
    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    recommendations.sort(
        key=lambda item: priority_order[item["priority"]]
    )

    return recommendations
