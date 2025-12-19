from datetime import datetime

""" 
Note: All of these validation functions will be run in a "enter values" function, 
when editing existing entries, and when importing or graphing data from a CSV
"""

# Create a dictionary to represent a daily entry
def create_daily_entry(
    date: str,
    hours_slept: int,
    exercise_minutes: int,
    mood_scale: float,
    mood_tags: str,
    activities: str,
    notes: str,
) -> tuple[dict, dict]:
    """
    Returns:
        entry: dict (empty if errors exist)
        errors: dict[field_name -> error_message]
    """

    errors = {}

    # --- Date ---
    if not validate_date(date):
        errors["date"] = "Invalid date. Please use YYYY-MM-DD."

    # --- Sleep ---
    if not validate_hours_slept(hours_slept):
        errors["hours_slept"] = "Sleep time must be between 0 and 1440 minutes."

    # --- Exercise ---
    if not validate_exercise_minutes(exercise_minutes):
        errors["exercise_minutes"] = "Exercise time must be between 0 and 1440 minutes."

    # --- Mood scale ---
    if not validate_mood_scale(mood_scale):
        errors["mood_scale"] = "Mood must be a number between 0 and 10."

    # --- Mood tags ---
    if not validate_mood_tags(mood_tags):
        errors["mood_tags"] = "Please enter at least one mood tag."

    # --- Activities ---
    if not validate_activities(activities):
        errors["activities"] = "Please enter at least one activity."

    # --- If any errors exist, do NOT build entry ---
    if errors:
        return {}, errors

    # --- Build clean entry only if valid ---
    entry = {
        "date": date,
        "hours_slept": hours_slept,
        "exercise_minutes": exercise_minutes,
        "mood_scale": float(mood_scale),
        "mood_tags": mood_tags.strip(),
        "activities": activities.strip(),
        "notes": notes.strip(),
    }

    return entry, {}


# Check that the date is valid, and is in a 'YYYY-MM-DD' format
def validate_date(date_str: str) -> bool:
    """
    Note: day and year will just be textboxes that only accept numbers, month will be a combo box.
    The values will be passed to this function as a string in the format 'YYYY-MM-DD'.
    Validates that the date string is in the format 'YYYY-MM-DD' and represents a valid date.
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Check that the time slept is within the bounds of 24 hours
def validate_hours_slept(hours_slept: int) -> bool:
    """
    Note - the textboxes will only accept number values enterred, and it won't register non-numeric input
    Note 2 - This function will also be used when editing, importing, and graphing data
    Note 3 - The user will enter the value in 'HH:MM' format, but it will be passed to this function as
        an integer representing total minutes
    """

    if hours_slept < 0 or hours_slept > 1440:
        return False
    return True

# Check that the exercise minutes is within the bounds of 24 hours
def validate_exercise_minutes(exercise_hours: int, exercise_minutes: int) -> bool:
    """
    Note - the textboxes will only accept number values enterred, and it won't register non-numeric input
    Note 2 - This function will also be used when editing, importing, and graphing data
    Note 3 - The user will enter the value in 'HH:MM' format, but it will be passed to this function as
        an integer representing total minutes
    """
    exmin = exercise_hours * 60 + exercise_minutes
    if exercise_minutes < 0 or exercise_minutes > 1440:
        return False
    return True

# Check that the mood scale is a float between 0 and 10.0
def validate_mood_scale(mood_scale) -> bool:
    """
    Note - the textboxes will only accept number values enterred, and it won't register non-numeric input
    Note 2 - This function will also be used when editing, importing, and graphing data
    Note 3 - Check for float between 0 and 10.0
    Note 4 - The value will be changed to 1 decimal place max, when saving to CSV, by the data IO functions
    """
    try:
        mood_value = float(mood_scale)
        if 0 <= mood_value <= 10.0:
            return True
        else:
            return False
    except ValueError:
        return False


def validate_mood_tags(mood_tags) -> bool:
    """
    Just a check to make sure that the user entered something, the user MUST enter something
    The entered descritpion will be parsed in ', ' separated values when saving to CSV, by the data IO functions
    """
    if mood_tags.strip():
        return True
    else:
        return False

def validate_activities(activities) -> bool:
   """
    Just a check to make sure that the user entered something, the user MUST enter something
    The entered descritpion will be parsed in ', ' separated values when saving to CSV, by the data IO functions
    """
   if activities.strip():
       return True
   else:
       return False
