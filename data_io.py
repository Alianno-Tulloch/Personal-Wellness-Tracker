"""
data_io.py

This file should do only storage:
- create CSV if missing
- read entries
- upsert (update if date exists, otherwise append)

Important:
- This file assumes it receives a VALID entry dict.
- Validation happens in data_validation.py.
"""

import csv
import os
from typing import Any


# The canonical column order for the CSV.
# Keeping a fixed order prevents weird "column order changes" later.
_FIELDNAMES = [
    "date",
    "sleep_minutes",
    "exercise_minutes",
    "mood_scale",
    "mood_tags",
    "activities",
    "notes",
]


def ensure_csv_exists(file_path: str) -> None:
    """
    Ensure the CSV exists and has a header row.
    If the file does not exist, create it and write the header.
    """
    folder = os.path.dirname(file_path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    if os.path.isfile(file_path):
        return

    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_FIELDNAMES)
        writer.writeheader()


def read_entries(file_path: str) -> list[dict[str, str]]:
    """
    Read CSV and return list of rows as dicts of strings.

    Note:
    - csv.DictReader returns all values as strings.
    - Later, for graphing, you can load with pandas and parse types.
    """
    ensure_csv_exists(file_path)

    with open(file_path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_entries(file_path: str, rows: list[dict[str, Any]]) -> None:
    """
    Overwrite the CSV with a new set of rows.

    rows can contain ints/floats, csv will write them as strings.
    """
    ensure_csv_exists(file_path)

    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_FIELDNAMES)
        writer.writeheader()

        # Ensure every row has all required keys, even if notes is empty
        for row in rows:
            safe_row = {k: row.get(k, "") for k in _FIELDNAMES}
            writer.writerow(safe_row)


def upsert_entry(file_path: str, entry: dict[str, Any]) -> str:
    """
    Upsert rule:
    - If entry["date"] already exists: replace that row
    - Else: append new row

    After updating, all rows are sorted by date (oldest -> newest)
    before being written back to the CSV.

    Returns:
    - "updated" or "inserted"
    """
    ensure_csv_exists(file_path)

    # Read existing rows (all values as strings)
    rows = read_entries(file_path)

    target_date = str(entry["date"])
    action = "inserted"
    updated_rows: list[dict[str, Any]] = []

    for row in rows:
        # Compare by date string; existing rows have string dates
        if row.get("date", "") == target_date:
            # Replace the old row with the new entry
            updated_rows.append(entry)
            action = "updated"
        else:
            updated_rows.append(row)

    # If no existing row matched, append as a new entry
    if action == "inserted":
        updated_rows.append(entry)

    # Sort rows by date string (YYYY-MM-DD sorts chronologically)
    updated_rows_sorted = sorted(
        updated_rows,
        key=lambda r: r.get("date", "")
    )

    # Write back to disk in sorted order
    write_entries(file_path, updated_rows_sorted)

    return action

def sort_csv_by_date(file_path: str) -> None:
    """
    Utility to resort the entire CSV by date.
    Can be called manually if you import / edit data outside the app.
    """
    rows = read_entries(file_path)
    rows_sorted = sorted(rows, key=lambda r: r.get("date", ""))
    write_entries(file_path, rows_sorted)
    