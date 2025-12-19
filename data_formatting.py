"""
data_formatting.py
Formatting/parsing helpers that are shared across UI, validation, and display.

Rule of thumb:
- *Parsing helpers* turn raw inputs into canonical stored values.
- *Formatting helpers* turn stored canonical values into human-readable strings.
"""

from typing import Optional
from datetime import datetime


# _MONTHS maps "normalized month strings" to month numbers.
_MONTHS = {
    "january": 1, "jan": 1, "1": 1, "01": 1,
    "february": 2, "feb": 2, "2": 2, "02": 2,
    "march": 3, "mar": 3, "3": 3, "03": 3,
    "april": 4, "apr": 4, "4": 4, "04": 4,
    "may": 5, "5": 5, "05": 5,
    "june": 6, "jun": 6, "6": 6, "06": 6,
    "july": 7, "jul": 7, "7": 7, "07": 7,
    "august": 8, "aug": 8, "8": 8, "08": 8,
    "september": 9, "sep": 9, "sept": 9, "9": 9, "09": 9,
    "october": 10, "oct": 10, "10": 10,
    "november": 11, "nov": 11, "11": 11,
    "december": 12, "dec": 12, "12": 12,
}

# Normalizes text and removes leading/trailing whitespace
def normalize_text(input: str) -> str:
    return input.strip().lower()


def month_to_number(month_text: str) -> Optional[int]:
    """
    Converts the Month text from the GUI combo box into an integer (1-12).
    Returns None if the input is invalid.

    Examples:
    - month_to_number(January) -> 1
    - month_to_number("Jan") -> 1
    - month_to_number("1") -> 1
    - month_to_number("Cake") -> None
    """
    input = normalize_text(month_text)
    return _MONTHS.get(input)

def hm_to_minutes(hours_text: str, minutes_text: str) -> int:
    """
    Converts the hours and minutes text from the GUI into total minutes,
    for use in the CSV file and data visualization.

    Returns None if either input isn't an integer.
    Examples:
    - hm_to_minutes("2", "5") -> 125
    """
    try:
        # Convert to integers, defaulting to 0 if the user entered nothing
        h = int(hours_text.strip() or "0")
        m = int(minutes_text.strip() or "0")
    except ValueError:
        return None
    
    return h * 60 + m

def minutes_to_hhmm(total_minutes: int) -> str:
    """
    Converts total minutes into "HH:MM" format, for use in GUI and
    data visualization.

    Example:
    - minutes_to_hhmm(125) -> "02:05"
    """
    # Might be redundant, because of minutes_to_human
    h = total_minutes // 60
    m = total_minutes % 60
    return f"{h:02d}:{m:02d}"

def minutes_to_human(total_minutes, str_type: int) -> str:
    """
    Converts total minutes into a human-readable string like 
    "2 hours 5 minutes", for use in GUI and data visualization.
    Also chooses between full and abbreviated forms based on context.
    str_type: 0 = full words, 1 = abbreviated

    Example:
    - minute_to_human(125, 0) -> "2 hours 5 minutes"
    - minute_to_human(125, 1) -> "2h 5mins"
    """
    h = total_minutes // 60
    m = total_minutes % 60
    time_str = ""

    if h > 0:
        if str_type == 0:
            hour_word = "hour" if h == 1 else "hours"
            time_str += f"{h}{hour_word} "
        elif str_type == 1:
            hour_word = "h"
            time_str += f"{h} {hour_word} "
    if m > 0:
        if str_type == 0:
            minute_word = "minute" if m == 1 else "minutes"
            time_str += f"{m} {minute_word} "
        elif str_type == 1:
            minute_word = "min" if m == 1 else "mins"
            time_str += f"{m}{minute_word}"
    time_str = time_str.strip()

    return time_str


def iso_date_to_human(iso_date: str) -> str:
    """
    Convert YYYY-MM-DD to 'January 1, 2025'. If invalid, returns original.

    Examples:
    - iso_date_to_human("2025-01-01") -> "January 1, 2025"
    """
    try:
        dt = datetime.strptime(iso_date, "%Y-%m-%d")
        return dt.strftime("%B %-d, %Y")
    except Exception: # For Windows compatibility, if %-d fails
        try:
            dt = datetime.strptime(iso_date, "%Y-%m-%d")
            return dt.strftime("%B %d, %Y").replace(" 0", " ")
        except Exception:
            return iso_date