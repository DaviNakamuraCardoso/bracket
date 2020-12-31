from django.shortcuts import render
from django.http import HttpResponseRedirect 
from clinics.models import Clinic
from clinics.utils import get_clinic 
# Create your views here.

def index(request): 
    """Render all the clinics in the same city as the user."""
        
    return render(request, 'base/index.html', {
        'user': request.user, 
        'clinics': Clinic.objects.all()
    })


def error(request): 
    """Return an error page for bad requests."""
    return render(request, 'base/error.html')