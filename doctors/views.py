from django.shortcuts import render, reverse 
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from doctors.models import Doctor, Appointment
from doctors.utils import get_doctor, make_schedule 
from doctors.forms import ShiftForm 
from clinics.utils import get_clinic, clinic_required
from base.models import Notification 
from users.data.time import get_weekday
import json 
# Create your views here.

def index(request): 
    return render(request, 'doctors/index.html', {
        'doctors': Doctor.objects.all()
    })


def profile(request, name): 
    doctor = get_doctor(name)
    return render(request, 'doctors/profile.html', {
        'doctor': doctor, 
        'data': doctor.serialize()
    })



def schedule_view(request, name): 
    doctor =  get_doctor(name)
    if len(doctor.clinics.all()) == 0: 
        return HttpResponseRedirect(reverse('base:index'))
        
    form = ShiftForm(user=request.user, initial={
        'start': "08:00:00", 
        'end': "18:00:00", 
        'clinic': doctor.clinics.all()[0]
    })
    if request.method == 'POST': 
        make_schedule(request)

    return render(request, 'doctors/schedule.html', {
        'doctor': doctor, 
        'form': form
    })


def schedule_days(request, name): 
    doctor = get_doctor(name)
    days = set()
    for shift in doctor.shifts.all(): 
        days.add(shift.day.day)
    
    return JsonResponse({'days': [day for day in days]})


def day_planner(request, name, year, month, day): 
    doctor = get_doctor(name)
    month += 1
    weekday = get_weekday(day, month, year)  
    try: 
        shifts = doctor.shifts.filter(day__day=weekday)
    except Shift.DoesNotExist: 
        return JsonResponse({"message": f"{doctor.__str__()} does not work on {weekday}."})

    day_appointments = []
    for shift in shifts: 
        day_appointments += shift.get_appointments()

    appointments = Appointment.objects.filter(day=day, month=month, year=year, shift__doctor=doctor)
    
    return JsonResponse({"day": day_appointments, "appointments":[appointment.index for appointment in appointments]})


def appointment_planner(request, name, year, month, day, index):
    doctor = get_doctor(name)
    month += 1
    weekday = get_weekday(day, month, year)
    shifts = doctor.shifts.filter(day__day=weekday) 

    counter = 0
    for shift in shifts: 
        appointments = shift.get_appointments()
        hour = appointments[index-counter]
        counter += len(appointments)
        if index <= counter: 

            return JsonResponse({'shift': shift.serialize(), 'hour': hour})
    
    return JsonResponse({"appointment": "Could not find!"})

    
@csrf_exempt 
@clinic_required  
def invite(request, name): 

    if request.method != "PUT": 
        return JsonResponse({"message": "Method must be PUT"})
    
    doctor = get_doctor(name=name)
    clinic = get_clinic(request) 
    data = json.loads(request.body)

    if not data['invite']: 
        notification = Notification.objects.get(user__name=name, origin=clinic.name)
        notification.delete()
        return JsonResponse({"message": "Your invitation has been removed"})

    
    invite_text = f"Is inviting you to work in their clinic"
    Notification.objects.create(user=doctor.user, text=invite_text, origin=clinic.name, url=reverse('clinics:invitation', args=(clinic.clinic_name, )))

    return JsonResponse({"message": "Invite sent succesfully."})


@csrf_exempt
def accept(request, name):
    if request.method != "PUT": 
        return JsonResponse({"message": "Method must be PUT"})
    
    clinic = get_clinic(request)
    doctor = get_doctor(name=name)
    data = json.loads(request.body)

    try: 
        request.user.notifications.get(origin=doctor.__str__()).delete()

    except Notification.DoesNotExist: 
        return JsonResponse({"message": "Could not accept the request. Probably, the user cancelled it."})
    
    if data['confirm']: 
        clinic.doctors.add(doctor)
        return JsonResponse({"message": "Succesfully accepted the doctor"})


    return JsonResponse({"message": "Succesfully refused to accept the user"})

