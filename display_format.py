
# This module provides utility functions to convert different value formats for display purposes.


def minutes_to_hhmm(total_minutes: int) -> str:
    h = total_minutes // 60
    m = total_minutes % 60
    return f"{h:02d}:{m:02d}"

def hhmm_to_minutes(hhmm: str) -> int:
    h, m = map(int, hhmm.split(':'))
    return (h * 60) + m