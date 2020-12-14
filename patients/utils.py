from math import floor


def strfdelta(years, months, days): 
    # Rounded numbers 
    y = floor(years)  
    m = floor(months)   
    d = round(days)

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