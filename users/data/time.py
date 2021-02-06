from datetime import datetime, time, timedelta 

MONTHS = [
    31, 
    31, 
    28, 
    31, 
    30, 
    31, 
    30, 
    31, 
    31, 
    30, 
    31, 
    30, 
    31
]


def get_calendar(month, year): 
    global MONTHS
    d = datetime(year=year, month=month, day=1)
    w = d.isoweekday()
    calendar = [0 for i in range(42)]
    month_days = MONTHS[month] if month != 2 and year % 4 != 0 else 29

    for i in range(w+1): 
        calendar[i] = MONTHS[month-1]-w+i+1

    for i in range(0, month_days): 
        calendar[i+w] = i+1 
    
    for i in range(0, 42-month_days-w): 
        calendar[month_days+i+w] = i+1


    return {"calendar": calendar, "start": w, "end": month_days+w} 


def delta(start, end):
    s1 = start.isoformat()
    s2 = end.isoformat()

    fmt = "%H:%M:%S"
    tdelta = datetime.strptime(s2, fmt) - datetime.strptime(s1, fmt)

    return tdelta


def sumtime(time_obj, tdelta): 
    s1 = time_obj.isoformat() 

    fmt = "%H:%M:%S"
    final = datetime.strptime(s1, fmt) + tdelta

    return final.strftime(fmt) 


def get_weekday(day, month, year): 

    date = datetime(year=year, month=month, day=day)

    return date.strftime("%A")
