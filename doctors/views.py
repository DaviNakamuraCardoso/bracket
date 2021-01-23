from django.shortcuts import render, reverse 
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from doctors.models import Doctor 
from doctors.utils import get_doctor 
from clinics.utils import get_clinic, clinic_required  
from base.models import Notification 
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
        request.user.notifications.get(origin=doctor.user.name).delete()

    except Notification.DoesNotExist: 
        return JsonResponse({"message": "Could not accept the request. Probably, the user cancelled it."})
    
    if data['confirm']: 
        clinic.doctors.add(doctor)
        return JsonResponse({"message": "Succesfully accepted the doctor"})


    return JsonResponse({"message": "Succesfully refused to accept the user"})

