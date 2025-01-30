from datetime import datetime, timedelta


def generate_working_days_for_next_weeks(weeks: int):
    today = datetime.today()
    next_monday = today + timedelta(days=(7 - today.weekday()))

    working_days = []
    for i in range(weeks * 7):
        current_day = next_monday + timedelta(days=i)
        if current_day.weekday() < 5:
            working_days.append(current_day)
    return working_days
