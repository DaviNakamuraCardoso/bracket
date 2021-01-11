from datetime import datetime, timezone
from math import floor


def intftimedelta(delta): 
    """Gets the number of years, months and days and returns a formatted string."""
    # Total years (float)
    years = delta.days / 365.25

    # From the float part of the years, get the months
    months = (years - floor(years)) * 365.25 / 30.4375 

    # ... months , get the days
    days = (months - floor(months)) * 30.4375


    #  days, get the hours 
    hours = (delta.seconds - (floor(days) * 24 * 60 * 60)) / 3600

    # ... hours, get the minutes
    minutes = (hours - floor(hours)) * 60

    # ... minutes, get the seconds
    seconds = (minutes - floor(minutes)) * 60


    # Rounded numbers 
    y = floor(years)  
    m = floor(months)   
    d = round(days)
    h = round(hours)
    minu = round(minutes)
    s = round(seconds)


    return {
        'seconds': s, 
        'minutes': minu, 
        'hours': h, 
        'days': d,   
        'months': m, 
        'years': y
    }


def strfdelta(delta):
    """Gets a timestamp and returns a proper string."""

    # Setting the values for months, days, hours, minutes and seconds
    time = [
        ['seconds', 60], 
        ['minutes', 60], 
        ['hours', 24], 
        ['days', 30],
        ['months', 12]

    ]

    ago = 1
    for order in time: 
        ago *= order[1]

        if  (delta.days * 3600 * 24 ) + delta.seconds < ago: 
            return f"{intftimedelta(delta)[order[0]]} {order[0]} ago"
    

    return f"{intftimedelta(delta)['years']} years ago"


        
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
 