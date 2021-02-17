from django.shortcuts import render, reverse 
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.postgres.search import TrigramSimilarity
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from doctors.models import Doctor, Appointment, Shift, Area
from doctors.utils import get_doctor, make_schedule 
from doctors.forms import ShiftForm 
from clinics.models import Clinic
from base.models import Notification 
from users.data.time import get_weekday
import json 
# Create your views here.

def index(request): 

    doctors = Doctor.objects.all()

    if search := request.GET.get('search_query'): 
        doctors = []
        results = Doctor.objects.annotate(
            similarity=TrigramSimilarity('user__name', search)
        ).all().order_by('-similarity')

        for doctor in results: 
            if doctor not in doctors: 
                doctors.append(doctor)

    return render(request, 'doctors/index.html', {
        'doctors': [doctor.serialize() for doctor in doctors] 
    })


def profile(request, name): 
    doctor = get_doctor(name)
    return render(request, 'doctors/profile.html', {
        'doctor': doctor, 
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
    user_appointments = Appointment.objects.filter(day=day, month=month, year=year, shift__doctor=doctor, user=request.user)
    
    return JsonResponse({"day": day_appointments, "appointments":[appointment.index for appointment in appointments], "user_appointments": [appointment.index for appointment in user_appointments]})


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
def invite(request, name, clinic_id): 

    if request.method != "PUT": 
        return JsonResponse({"message": "Method must be PUT"})
    
    doctor = Doctor.objects.get(user__name=name)
    clinic.doctors.add(doctor)
    

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


@login_required 
def new_appointment(request, name): 
    if request.method == "POST": 

        doctor = get_doctor(name)
        data = json.loads(request.body)
        patient = None
        if data['patient'] == request.user.first_name + " " + request.user.last_name: 
            patient = request.user.patient

        appointment = Appointment.objects.create(
            user=request.user, 
            patient=patient, 
            to=data['patient'], 
            shift=Shift.objects.get(pk=data['shift']), 
            day=data['day'], 
            month=data['month']+1, 
            year=data['year'], 
            index=data['index'], 
            area=Area.objects.get(area=data['area'])
            
        )
        return JsonResponse({"message": f"Appointment scheduled successfully."})
    
    return JsonResponse({"message": "Method must be POST."})
