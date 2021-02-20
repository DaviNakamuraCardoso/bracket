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

TIMEZONES = {
    'America/Adak': -4,
    'America/Anchorage': -3,
    'America/Araguaina': 3,
    'America/Bahia': 3,
    'America/Belem': 3,
    'America/Boa_Vista': 2,
    'America/Campo_Grande': 2,
    'America/Cuiaba': 2,
    'America/Chicago': 0,
    'America/Denver': -1,
    'America/Detroit': -1,
    'America/Eirunepe': 1,
    'America/Fortaleza': 3,
    'America/Indiana/Indianapolis': 1,
    'America/Indiana/Knox': 0,
    'America/Indiana/Marengo': 1,
    'America/Indiana/Petersburg': 1,
    'America/Indiana/Tell_City': 0,
    'America/Indiana/Vevay': 1,
    'America/Indiana/Vincennes': 1,
    'America/Indiana/Winamac': 1,
    'America/Indianapolis': 1,
    'America/Juneau': -3,
    'America/Kentucky/Louisville': 1,
    'America/Kentucky/Monticello': 1,
    'America/Knox_IN': 0,
    'America/Los_Angeles': -2,
    'America/Louisville': -1,
    'America/Maceio': 3,
    'America/Manaus': 2,
    'America/New_York': 1,
    'America/Noronha': 4,
    'America/Phoenix': -1,
    'America/Porto_Acre': 1,
    'America/Porto_Velho': 2,
    'America/Recife': 3,
    'America/Rio_Branco': 1,
    'America/Santarem': 3,
    'America/Sao_Paulo': 3,
    'America/Shiprok': -1,
    'America/Sitka': -3,
    'America/Yakutat': -3
}

def tz(timezone):
    global TIMEZONES
    return TIMEZONES[timezone.strip(' ')]

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
