from datetime import datetime, timezone
from math import floor


def intftimedelta(timedelta=None, timestamp=None):
    """
        Gets a timedelta or a timestamp and returns a dictionary with
        the number of seconds, minutes, hours, days, months and years.
    """

    if timestamp is not None:
        delta = datetime.now(timezone.utc) - timestamp

    else:
        delta = timedelta

    # Total years (float)
    years = delta.days / 365.25

    # From the float part of the years, get the months
    months = (years - floor(years)) * 365.25 / 30.4375

    # ... months , get the weeks
    weeks = (months - floor(months)) * 30.4375 / 7

    # ... weeks , get the days
    days = (weeks - floor(weeks)) * 7

    #  days, get the hours
    hours = (delta.seconds - (floor(days) * 24 * 60 * 60)) / 3600

    # ... hours, get the minutes
    minutes = (hours - floor(hours)) * 60

    # ... minutes, get the seconds
    seconds = (minutes - floor(minutes)) * 60


    # Rounded numbers
    y = floor(years)
    m = floor(months)
    w = round(weeks)
    d = floor(days)
    h = floor(hours)
    minu = floor(minutes)
    s = floor(seconds)


    return {
        'seconds': s,
        'minutes': minu,
        'hours': h,
        'days': d,
        'weeks': w,
        'months': m,
        'years': y
    }


def strfdelta(timedelta=None, timestamp=None):
    """Gets a timestamp and returns a proper string."""

    if timestamp is not None:
        delta = datetime.now(timezone.utc) - timestamp
    else:
        delta = timedelta

    # Setting the values for months, days, hours, minutes and seconds
    time = [
        ['seconds', 60],
        ['minutes', 60],
        ['hours', 24],
        ['days', 7],
        ['weeks', 30.4375 / 7],
        ['months', 12]

    ]

    ago = 1
    for order in time:
        ago *= order[1]

        if  (delta.days * 3600 * 24 ) + delta.seconds < ago:
            number = max(1, intftimedelta(delta)[order[0]])
            word = order[0] if number > 1 else order[0].rstrip('s')

            return f"{number} {word} ago"

    number = intftimedelta(delta)['years']
    word = 'years' if number > 1 else 'year'
    return f"{number} {word} ago"



def strfage(d, m, y):
    """
        Gets the exact number of days, months and years and
        returns a string with patient's age.
    """
    # Strings for years, months and days
    ys = f"{y} years" if y > 1 else f"One year"
    ms = f"{m} months" if m > 1 else f"one month"
    ds = f"{d} days" if d > 1 else f"one day"

    # Empty string if the number is 0
    fy = ys if y >= 1 else ""
    fm = ms if m >= 1 else ""
    fd = ds if d >= 1 else ""

    # If all the strings are empty, the patient was born today
    if fy == fm == fd == "":
        return "Born today."

    # Returns the right string for days, months and years
    return f"{fy} {fm} {fd}"
