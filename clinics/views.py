from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from clinics.models import Clinic 
from base.models import Notification
from doctors.utils import get_doctor
from clinics.utils import get_clinic
import json 

# Create your views here.

def index(request): 
    return render(request, 'clinics/index.html')


def profile(request, clinic_name): 
    try: 
        clinic  = Clinic.objects.get(clinic_name=clinic_name)
    except Clinic.DoesNotExist: 
        return HttpResponse('Error 404')
    
    return render(request, 'clinics/profile.html', {
        'clinic': clinic, 
        'data': clinic.serialize()
    })


@csrf_exempt 
def invitation(request, clinic_name): 
    if request.method != "PUT": 
        return JsonResponse({"message": "Method must be PUT"})

    clinic = Clinic.objects.get(clinic_name=clinic_name)
    doctor = request.user.doctor
    data = json.loads(request.body)

    # In both cases, the notification is deleted 
    try: 
        request.user.notifications.get(origin=clinic.name).delete()

    except Notification.DoesNotExist: 
        # If there is no notification to delete, it means that the clinic cancelled the invitation
        return JsonResponse({"message": "Could not join the accept the invitation. The clinic probably canceled it."})

    if data['confirm']: 
        clinic.doctors.add(doctor)
        return JsonResponse({"message": "Succesfully joined the clinic."}) 
    
    return JsonResponse({"message": "Succesfully refused to join the clinic."}) 

@csrf_exempt 
def join(request, name): 
    if request.method != "PUT": 
        return JsonResponse({"message": "Method must be PUT"})

    doctor = get_doctor(request=request)
    clinic = get_clinic(name=name)
    data = json.loads(request.body)

    if data['invite']: 
        notification = Notification.objects.get(origin=doctor.user.name, user__name=clinic.user.name)
        notification.delete()

        return JsonResponse({"message": "Join request cancelled succesfully"})

    invite_text = f"Is asking to join {clinic.name}"
    invite_url = reverse('doctors:accept', args=(doctor.user.name, ))
    Notification.objects.create(user=clinic.user, text=invite_text, url=invite_url)

    return JsonResponse({"message": "Request sent succesfully."})







    

    