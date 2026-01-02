"""
data_validation.py

You specifically wanted:
- Validation functions separate from create_daily_entry
- create_daily_entry just coordinates parsing + validation and returns (entry, errors)
- Validators reusable for imports, editing, graph cleaning

Pattern used here:
- validate_* functions return:
    - None if valid
    - an error message string if invalid

That is easier for the GUI:
- if message exists, display it beside that field
- also can build a full "error panel" list
"""

from datetime import datetime
from typing import Optional, Tuple, Any

from data_formatting import month_to_number, hm_to_minutes


# -----------------------------
# Parsing helpers (string -> number)
# These are reusable too, because imports might start as strings.
# -----------------------------

def parse_int(text: str, field_name: str) -> Tuple[Optional[int], Optional[str]]:
    """
    Try to parse an integer from a string.

    Returns:
    - (int_value, None) if OK
    - (None, error_message) if invalid
    """
    cleaned = text.strip()
    if cleaned == "":
        return None, f"{field_name} is required."
    try:
        return int(cleaned), None
    except ValueError:
        return None, f"{field_name} must be a whole number."


def parse_float(text: str, field_name: str) -> Tuple[Optional[float], Optional[str]]:
    """
    Try to parse a float from a string.

    Returns:
    - (float_value, None) if OK
    - (None, error_message) if invalid
    """
    cleaned = text.strip()
    if cleaned == "":
        return None, f"{field_name} is required."
    try:
        return float(cleaned), None
    except ValueError:
        return None, f"{field_name} must be a number (example: 7.5)."


# -----------------------------
# Validators (typed values -> error message or None)
# These should be reusable across the entire app.
# -----------------------------

def validate_iso_date(iso_date: str) -> Optional[str]:
    """
    Validate that a string is a real date in YYYY-MM-DD format.
    """
    try:
        datetime.strptime(iso_date, "%Y-%m-%d")
        return None
    except ValueError:
        return "Invalid date."


def validate_total_minutes(total_minutes: int, field_name: str) -> Optional[str]:
    """
    Validate 0..1440 minutes (0 to 24 hours).
    """
    if total_minutes < 0 or total_minutes > 1440:
        return f"{field_name} must be between 0 and 24 hours."
    return None


def validate_mood_scale(mood_scale: float) -> Optional[str]:
    """
    Mood scale must be between 0.0 and 10.0 inclusive.
    """
    if mood_scale < 0.0 or mood_scale > 10.0:
        return "Mood scale must be between 0.0 and 10.0."
    return None


def validate_required_text(text: str, field_name: str) -> Optional[str]:
    """
    Required text fields must not be blank.
    """
    if text.strip() == "":
        return f"{field_name} is required."
    return None


# -----------------------------
# Builder / coordinator
# This is what the GUI calls on submit.
# It returns (entry_dict, errors_dict).
# -----------------------------

def create_daily_entry(
    date_day_text: str,
    date_month_text: str,
    date_year_text: str,
    sleep_hours_text: str,
    sleep_minutes_text: str,
    exercise_hours_text: str,
    exercise_minutes_text: str,
    mood_scale_text: str,
    mood_tags_text: str,
    activities_text: str,
    notes_text: str,
) -> tuple[dict[str, Any], dict[str, str]]:
    """
    Build a canonical entry dict from raw GUI strings.

    Returns:
    - entry dict if valid, otherwise {}
    - errors dict mapping field_key -> message

    Canonical schema (what should be saved to CSV):
    - date: "YYYY-MM-DD"
    - sleep_minutes: int
    - exercise_minutes: int
    - mood_scale: float (rounded to 1 decimal)
    - mood_tags: str (raw comma-separated string for now)
    - activities: str (raw comma-separated string for now)
    - notes: str
    """
    errors: dict[str, str] = {}

    # -------------------------
    # Date parsing
    # -------------------------

    day_val, day_err = parse_int(date_day_text, "Day")
    if day_err:
        errors["date_day"] = day_err

    year_val, year_err = parse_int(date_year_text, "Year")
    if year_err:
        errors["date_year"] = year_err

    month_num = month_to_number(date_month_text)
    if month_num is None:
        errors["date_month"] = "Month must be a real month (example: January)."

    iso_date: Optional[str] = None
    if "date_day" not in errors and "date_year" not in errors and "date_month" not in errors:
        # Build YYYY-MM-DD and validate via datetime to catch leap years etc.
        iso_candidate = f"{year_val:04d}-{month_num:02d}-{day_val:02d}"
        date_err = validate_iso_date(iso_candidate)
        if date_err:
            errors["date"] = "That date does not exist."
        else:
            iso_date = iso_candidate

    # -------------------------
    # Sleep time parsing
    # Your rule: one blank allowed, but not both blank.
    # -------------------------

    sleep_total = hm_to_minutes(sleep_hours_text, sleep_minutes_text, require_any=True)
    if sleep_total is None:
        errors["sleep_time"] = "Sleep time must include hours or minutes (numbers only)."
    else:
        sleep_range_err = validate_total_minutes(sleep_total, "Sleep time")
        if sleep_range_err:
            errors["sleep_time"] = sleep_range_err

    # -------------------------
    # Exercise time parsing
    # -------------------------

    exercise_total = hm_to_minutes(exercise_hours_text, exercise_minutes_text, require_any=True)
    if exercise_total is None:
        errors["exercise_time"] = "Exercise time must include hours or minutes (numbers only)."
    else:
        exercise_range_err = validate_total_minutes(exercise_total, "Exercise time")
        if exercise_range_err:
            errors["exercise_time"] = exercise_range_err

    # -------------------------
    # Mood scale parsing
    # -------------------------

    mood_val, mood_parse_err = parse_float(mood_scale_text, "Mood scale")
    if mood_parse_err:
        errors["mood_scale"] = mood_parse_err
    elif mood_val is not None:
        mood_rule_err = validate_mood_scale(mood_val)
        if mood_rule_err:
            errors["mood_scale"] = mood_rule_err

    # -------------------------
    # Required text fields
    # -------------------------

    mood_tags_err = validate_required_text(mood_tags_text, "Mood tags")
    if mood_tags_err:
        errors["mood_tags"] = mood_tags_err

    activities_err = validate_required_text(activities_text, "Activities")
    if activities_err:
        errors["activities"] = activities_err

    # Notes are optional, so only normalize whitespace.
    notes_clean = notes_text.strip()

    # If anything failed, do not build an entry.
    if errors:
        return {}, errors

    # At this point, everything is valid and typed.
    entry: dict[str, Any] = {
        "date": iso_date,
        "sleep_minutes": int(sleep_total),
        "exercise_minutes": int(exercise_total),
        "mood_scale": round(float(mood_val), 1),
        "mood_tags": mood_tags_text.strip(),
        "activities": activities_text.strip(),
        "notes": notes_clean,
    }

    return entry, {}
