from django.shortcuts import render
from django.http import HttpResponse
from doctors.models import Doctor 

# Create your views here.

def index(request): 
    return render(request, 'doctors/index.html')


def profile(request, name): 
    try: 
        doctor = Doctor.objects.get(user__name=name)
    except Doctor.DoesNotExist: 
        return HttpResponse("Error 404")
    
    return render(request, 'doctors/profile.html', {
        'doctor': doctor, 
        'data': doctor.serialize()
    })