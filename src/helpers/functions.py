from datetime import datetime
import pytz


def format_datetime_from_date(s: str):
    return datetime.fromisoformat(s)

def format_date_from_date(s: str):
    dt = datetime.fromisoformat(s)
    
    if dt.year != datetime.today().year:
        fmt_str = '%b %#d, %Y'
    else:
        fmt_str = '%a, %b %#d'

    date = datetime.strftime(dt, fmt_str)

    return date

def format_time_from_date(s: str):
    dt = datetime.fromisoformat(s)
    
    # 2. Define the target timezone (Central Time)
    central_timezone = pytz.timezone('America/Chicago')

    # 3. Convert the datetime object to the target timezone
    central_datetime = dt.astimezone(central_timezone)
    
    time = central_datetime.strftime("%#I:%M %p")
    return time