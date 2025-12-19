
# This module provides utility functions to convert different value formats for display purposes.


def minutes_to_hours_minutes(total_minutes: int) -> str:
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours}h {minutes}m"

def hours_minutes_to_minutes(hours: int, minutes: int) -> str:
    total_minutes = hours * 60 + minutes
    return str(total_minutes)