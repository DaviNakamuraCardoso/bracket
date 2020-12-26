from math import floor
from django.http import HttpResponseRedirect
from django.shortcuts import reverse  


def strfdelta(timedelta): 
    """Gets the number of years, months and days and returns a formatted string."""
    # Total years (float)
    years = age.days / 365.25

    # From the float part of the years, get the months
    months = (years - math.floor(years)) * 365.25 / 30.4375 

    # From the float part of the months, get the days
    days = (months - math.floor(months)) * 30.4375


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
    

def patient(function): 
    def inner(request, *args, **kwargs): 
        if request.user.is_authenticated: 
            if request.user.is_patient: 
                return function(request, *args, **kwargs)
        
        return HttpResponseRedirect(reverse('base:error'))
    
    return inner 






