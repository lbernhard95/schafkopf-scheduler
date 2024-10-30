from datetime import datetime, timedelta
from typing import List, Optional

from schafkopf.core.bitpoll import VoteDate



def generate_working_days_for_next_weeks(weeks: int):
    today = datetime.today()
    next_monday = today + timedelta(days=(7 - today.weekday()))
    
    working_days = []
    for i in range(weeks * 7):
        current_day = next_monday + timedelta(days=i)
        if current_day.weekday() < 5:
            working_days.append(current_day)
    return working_days



def find_best_date(votes: List[VoteDate]) -> Optional[VoteDate]:
    eligible_votes = [vote for vote in votes if vote.yes_count >= 4]
    if not eligible_votes:
        return None
    return max(
        eligible_votes, 
        key=lambda vote: vote.attendance_probability
    )
