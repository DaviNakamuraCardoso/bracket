from django.shortcuts import render
from django.http import HttpResponse 
from clinics.models import Clinic 

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
    
