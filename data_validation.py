from datetime import datetime

""" 
Note: All of these validation functions will be run in a "enter values" function, 
when editing existing entries, and when importing or graphing data from a CSV
"""

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

# Check that the time slept is saved in a 'HH:MM' format
def validate_hours_slept(hours_slept):
    """
    # Note - the textboxes will only accept number values enterred, and it won't register non-numeric input
    # Note 2 - This function will also be used when editing, importing, and graphing data
    # Note 3 - change to check for 'HH:MM' format
    """
    try:
        datetime.strptime(hours_slept, '%H:%M')
        return True
    except ValueError:
        return False

def validate_exercise_minutes(exercise_minutes):
    """
    # Note - the textboxes will only accept number values enterred, and it won't register non-numeric input
    # Note 2 - This function will also be used when editing, importing, and graphing data
    # Note 3 - change to check for 'HH:MM' format
    """

    try:
        datetime.strptime(exercise_minutes, '%H:%M')
        return True
    except ValueError:
        return False

# Check that the mood scale is a float between 0 and 10.0
def validate_mood_scale(mood_scale):
    """
    # Note - the textboxes will only accept number values enterred, and it won't register non-numeric input
    # Note 2 - This function will also be used when editing, importing, and graphing data
    # Note 3 - Check for float between 0 and 10.0
    # Note 4 - The value will be changed to 1 decimal place max, when saving to CSV, by the data IO functions
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
    # Just a check to make sure that the user entered something, the user MUST enter something
    # The entered descritpion will be parsed in ', ' separated values when saving to CSV, by the data IO functions
    """
    if mood_tags.strip():
        return True
    else:
        return False

def validate_activities(activities):
   """
    # Just a check to make sure that the user entered something, the user MUST enter something
    # The entered descritpion will be parsed in ', ' separated values when saving to CSV, by the data IO functions
    """
   if activities.strip():
       return True
   else:
       return False
