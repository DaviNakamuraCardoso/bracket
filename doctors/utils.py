from django.http import HttpResponseRedirect 
from django.shortcuts import reverse 
from doctors.models import Doctor, Shift, Area
from clinics.models import Clinic
from users.models import Day
from datetime import timedelta


def get_doctor(name=None, request=None): 
    """Receive a name and returns a doctor object."""
    if request is not None: 
        if request.user.is_authenticated: 
            if request.user.is_doctor: 
                return request.user.doctor 
        return HttpResponseRedirect(reverse('base:error'))


    try: 
        doctor = Doctor.objects.get(user__name=name)
    except Doctor.DoesNotExist: 
        return HttpResponseRedirect(reverse('base:error'))
    return doctor 
    
    
def get_user_doctor(request): 
    """Receive the request and returns the current doctor."""
    if request.user.is_authenticated: 
        if request.user.is_doctor: 
            return request.user.doctor 

    
    return HttpResponseRedirect(reverse('base:error'))


def doctor(function): 
    def inner(request, *args, **kwargs): 
        if request.user.is_authenticated: 
            if request.user.is_patient: 
                return function(request, *args, **kwargs)
        

        return HttpResponseRedirect(reverse('base:error'))
    
    return inner 


def make_schedule(request): 
    data = request.POST
    days = data['days'].split()
    for day in days: 
        for i in data[f"{day}_num"]: 
            shift = Shift.objects.create(
                doctor=request.user.doctor, 
                day=Day.objects.get(day=day), 
                duration=timedelta(hours=float(data[daystr(day, i, 'duration_hours')]), minutes=float(data[daystr(day, i, 'duration_minutes')])), 
                start=data[daystr(day, i, 'start')], 
                end=data[daystr(day, i, 'end')], 
                clinic=Clinic.objects.get(pk=data[daystr(day, i, 'clinic')])
                
            )
            for j in [area.id for area in request.user.doctor.areas.all()]: 
                # WAAAAAAAAAAAAAALRUSSSSSS
                if area_id := data[f"areas_{j}_{day}_{i}"]:
                
                    shift.areas.add(Area.objects.get(pk=area_id))
            if data[daystr(day, i, 'break_time')] != '' and data[daystr(day, i, 'break_time')] != '': 
                shift.break_time = data[daystr(day, i, 'break_time')]
                shift.break_end = data[daystr(day, i, 'break_end')]


def daystr(day, i, string): 
    return f"{string}_{day}_{i}"
    