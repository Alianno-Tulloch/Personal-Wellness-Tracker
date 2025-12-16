"""
This file handles data structures and user inputs for a personal health tracking application.
"""



def create_daily_entry(
    date,
    hours_slept,
    exercise_minutes,
    mood_scale,
    mood_description,
    activities,
    notes,
):
    return{
    "date": date,               # string in YYYY-MM-DD format
    "hours_slept": hours_slept,     # float representing hours slept
    "exercise_minutes": exercise_minutes,  # integer representing minutes of exercise
    "mood_scale": mood_scale,        # integer from 1 to 10
    "mood_description": mood_description, # string describing mood (e.g., "happy", "stressed")
    "activities": [],       # list of strings representing activities
    "notes": ""             # string for additional notes
}

# Test Entry
test_entry = {
    "date": "2024-06-15",
    "hours_slept": 7.5,
    "exercise_minutes": 45,
    "mood_scale": 8,
    "mood_description": "happy",
    "activities": "jogging, reading, cooking",
    "notes": "Had a great day exploring new recipes and enjoying the sunshine.\
        Felt energetic and positive throughout the day."
}

"""
Note for when implementing the GUI:
- Tell the user to separate their activities using commas, so it can be parsed correctly by the getter

"""