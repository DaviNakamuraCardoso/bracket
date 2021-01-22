from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required 
from patients.models import Patient

# Create your views here.


def index(request): 
    return render(request, 'patients/index.html', {
        'patients': Patient.objects.all()
    })
@login_required 
def profile(request, name): 
    try: 
        patient = Patient.objects.get(user__name=name)
    except Patient.DoesNotExist: 
        return HttpResponse("Error 404")
    return render(request, 'patients/profile.html', {
        'patient': patient, 
        'data': patient.serialize()
    })
