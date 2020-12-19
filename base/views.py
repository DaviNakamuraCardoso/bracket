from django.shortcuts import render
from django.http import HttpResponseRedirect 
from clinics.models import Clinic


# Create your views here.

def index(request): 
    if request.user.is_clinic: 
        clinic = Clinic.objects.get(user__name=request.user.name)
        
    return render(request, 'base/index.html', {
        'user': request.user, 
        'clinic': clinic 
    })