from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from clinics.models import Clinic 
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
    clinic = Clinic.objects.get(clinic_name=clinic_name)
    doctor = request.user.doctor
    if request.method == "PUT": 
        data = json.loads(request.body)
        if data['confirm']: 
            clinic.doctors.add(doctor)
            return JsonResponse({"message": f"Succesfully joined {clinic.name}"}, status=204)
        else: 
            request.user.notifications.get(origin=clinic.name).delete()
            return JsonResponse({"message": f"Succesfully refused to join {clinic.name}"}, status=204) 
    
    return JsonResponse({"message": "Method must be PUT."}, status=400)
            


    

        

    
