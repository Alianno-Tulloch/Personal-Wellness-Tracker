import csv
import os


# Rounds the mood scale to one decimal place
def round_mood_scale(mood_scale):
    return round(float(mood_scale), 1)

# Parses the mood tags from a comma-separated string into a list
def parse_mood_tags(mood_tags_str):
    return [tag.strip() for tag in mood_tags_str.split(',') if tag.strip()]

# Parses the activities from a comma-separated string into a list
def parse_activities(activities_str):
    return [activity.strip() for activity in activities_str.split(',') if activity.strip()]

def upsert_entry(file_path, data_entry):
    file_exists = os.path.isfile(file_path)
