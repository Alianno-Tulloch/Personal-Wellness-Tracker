"""
data_formatting.py

Formatting/parsing helpers that are shared across:
- GUI
- validation
- display (later, for graph hover text, etc.)

Rule of thumb:
- Parsing helpers: take messy raw inputs and convert them into canonical stored values.
- Formatting helpers: take canonical stored values and convert them into human-readable text.

Important note about naming:
- _MONTHS starts with an underscore. In Python, that is a convention meaning:
  "this is intended for internal/private use inside this module".
  It does not enforce privacy, it is just a signal to the reader.
"""

from datetime import datetime
from typing import Optional


# Maps common month inputs to month numbers.
# We accept:
# - full names: "January"
# - abbreviations: "Jan"
# - numbers: "1", "01"
# This lets your editable combo box accept typed values safely.
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


def normalize_text(text: str) -> str:
    """
    Lowercase + trim whitespace.
    This helps month parsing accept '  Jan  ' and treat it as 'jan'.
    """
    return text.strip().lower()


def month_to_number(month_text: str) -> Optional[int]:
    """
    Convert month text to an integer month number (1-12).
    Returns None if invalid.

    Examples:
    - month_to_number("January") -> 1
    - month_to_number("jan") -> 1
    - month_to_number("1") -> 1
    - month_to_number("pizza") -> None
    """
    key = normalize_text(month_text)
    return _MONTHS.get(key)


def hm_to_minutes(hours_text: str, minutes_text: str, require_any: bool) -> Optional[int]:
    """
    Convert hours + minutes text into total minutes.

    Your rule:
    - Allow one blank if the other is filled.
    - If BOTH are blank, that is invalid for required fields.

    We implement that with `require_any`:
    - If require_any is True and both fields are blank -> return None (invalid).
    - Otherwise blank fields become 0.

    Returns:
    - int total minutes if parsing works
    - None if parsing fails or both blank (when require_any is True)
    """
    h_clean = hours_text.strip()
    m_clean = minutes_text.strip()

    # If both are blank and the field is required, treat as invalid.
    if require_any and h_clean == "" and m_clean == "":
        return None

    # If one is blank, treat it as 0 (allowed by your accessibility rule).
    if h_clean == "":
        h_clean = "0"
    if m_clean == "":
        m_clean = "0"

    try:
        h = int(h_clean)
        m = int(m_clean)
    except ValueError:
        return None

    return (h * 60) + m


def minutes_to_hhmm(total_minutes: int) -> str:
    """
    Convert minutes -> 'HH:MM' (always 2 digits each).

    Example:
    - minutes_to_hhmm(125) -> "02:05"
    """
    h = total_minutes // 60
    m = total_minutes % 60
    return f"{h:02d}:{m:02d}"


def minutes_to_human(total_minutes: int, abbreviated: bool) -> str:
    """
    Convert minutes -> human-readable text.
    This will be useful later for graph hover labels.

    abbreviated:
    - False: "2 hours 5 minutes"
    - True:  "2h 5min"

    Examples:
    - minutes_to_human(125, False) -> "2 hours 5 minutes"
    - minutes_to_human(125, True)  -> "2h 5min"
    """
    h = total_minutes // 60
    m = total_minutes % 60

    parts = []

    if h > 0:
        if abbreviated:
            parts.append(f"{h}h")
        else:
            hour_word = "hour" if h == 1 else "hours"
            parts.append(f"{h} {hour_word}")

    if m > 0:
        if abbreviated:
            parts.append(f"{m}min")
        else:
            minute_word = "minute" if m == 1 else "minutes"
            parts.append(f"{m} {minute_word}")

    # If both are 0, return "0 minutes" or "0min"
    if not parts:
        return "0min" if abbreviated else "0 minutes"

    return " ".join(parts)


def iso_date_to_human(iso_date: str) -> str:
    """
    Convert 'YYYY-MM-DD' -> 'January 1, 2025'

    We avoid platform-specific strftime day formatting issues by using dt.day.
    """
    try:
        dt = datetime.strptime(iso_date, "%Y-%m-%d")
        # dt.day gives an int day number without leading zeros, cross-platform.
        return f"{dt.strftime('%B')} {dt.day}, {dt.year}"
    except ValueError:
        # If it's invalid, just return the raw string.
        return iso_date
