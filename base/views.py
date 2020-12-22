from django.shortcuts import render
from django.http import HttpResponseRedirect 
from clinics.models import Clinic
from clinics.utils import get_clinic 
# Create your views here.

def index(request): 
        
    return render(request, 'base/index.html', {
        'user': request.user, 
        'clinic': get_clinic(request) 
    })