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
) -> dict:
    return {
        "date": date,               # string in YYYY-MM-DD format
        "hours_slept": hours_slept,     # hours slept in minutes
        "exercise_minutes": exercise_minutes,  # hours exercised in minutes
        "mood_scale": mood_scale,        # integer from 1 to 10
        "mood_tags": mood_tags, # string describing mood (e.g., "happy", "stressed")
        "activities": activities,       # list of strings representing activities
        "notes": notes             # string for additional notes
    }


# Check that the date is valid, and is in a 'YYYY-MM-DD' format
def validate_date(date_str):
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
def validate_hours_slept(hours_slept):
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
def validate_exercise_minutes(exercise_minutes):
    """
    Note - the textboxes will only accept number values enterred, and it won't register non-numeric input
    Note 2 - This function will also be used when editing, importing, and graphing data
    Note 3 - The user will enter the value in 'HH:MM' format, but it will be passed to this function as
        an integer representing total minutes
    """
    if exercise_minutes < 0 or exercise_minutes > 1440:
        return False
    return True

# Check that the mood scale is a float between 0 and 10.0
def validate_mood_scale(mood_scale):
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


def validate_mood_tags(mood_tags):
    """
    Just a check to make sure that the user entered something, the user MUST enter something
    The entered descritpion will be parsed in ', ' separated values when saving to CSV, by the data IO functions
    """
    if mood_tags.strip():
        return True
    else:
        return False

def validate_activities(activities):
   """
    Just a check to make sure that the user entered something, the user MUST enter something
    The entered descritpion will be parsed in ', ' separated values when saving to CSV, by the data IO functions
    """
   if activities.strip():
       return True
   else:
       return False
