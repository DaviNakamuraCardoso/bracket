from django.shortcuts import render
from django.http import HttpResponseRedirect 
from clinics.models import Clinic
from users.forms import PatientForm, BaseForm
# Create your views here.

def index(request): 
    """Render all the clinics in the same city as the user."""
    form = PatientForm()
    base_form = BaseForm()
        
    return render(request, 'base/index.html', {
        'user': request.user, 
        'clinics': Clinic.objects.all(), 
        'form': form, 
        'base_form': base_form 
    })


def error(request): 
    """Return an error page for bad requests."""
    return render(request, 'base/error.html')