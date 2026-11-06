
import hashlib
from collections import defaultdict
from pathlib import Path


CHUNK_SIZE = 65536


def calculate_partial_hash(file_path):
    """Create a quick fingerprint using the beginning and end of a file."""

    try:
        path = Path(file_path)

        with path.open("rb") as file:
            first_chunk = file.read(CHUNK_SIZE)

            file.seek(max(0, path.stat().st_size - CHUNK_SIZE))
            last_chunk = file.read(CHUNK_SIZE)

        fingerprint = hashlib.sha256()
        fingerprint.update(first_chunk)
        fingerprint.update(last_chunk)

        return fingerprint.hexdigest()

    except (OSError, PermissionError):
        return None


def calculate_file_hash(file_path):
    """Calculate the complete SHA-256 hash."""

    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            for chunk in iter(
                lambda: file.read(CHUNK_SIZE), b""
            ):
                sha256.update(chunk)

        return sha256.hexdigest()

    except (OSError, PermissionError):
        return None


def find_duplicates(files):
    """Find duplicate files using size, partial hash, and full hash."""

    size_groups = defaultdict(list)

    # Stage 1: Group files by size.
    for file in files:
        size_groups[file["size"]].append(file)

    partial_groups = defaultdict(list)

    # Stage 2: Compare partial fingerprints.
    for matching_files in size_groups.values():

        if len(matching_files) < 2:
            continue

        for file in matching_files:
            fingerprint = calculate_partial_hash(file["path"])

            if fingerprint:
                partial_groups[
                    (file["size"], fingerprint)
                ].append(file)

    full_hash_groups = defaultdict(list)

    # Stage 3: Verify candidates using complete SHA-256 hashes.
    for matching_files in partial_groups.values():

        if len(matching_files) < 2:
            continue

        for file in matching_files:
            file_hash = calculate_file_hash(file["path"])

            if file_hash:
                full_hash_groups[file_hash].append(file)

    return {
        file_hash: group
        for file_hash, group in full_hash_groups.items()
        if len(group) > 1
    }
