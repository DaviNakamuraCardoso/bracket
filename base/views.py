from django.shortcuts import render
from django.http import HttpResponseRedirect 
from clinics.models import Clinic
from clinics.utils import get_clinic 
from users.forms import RegisterForm
# Create your views here.

def index(request): 
    """Render all the clinics in the same city as the user."""
    form = RegisterForm()

    if request.method == "POST": 
        form = RegisterForm(request.POST)
        
    return render(request, 'base/index.html', {
        'user': request.user, 
        'clinics': Clinic.objects.all(), 
        'form': form
    })


def error(request): 
    """Return an error page for bad requests."""
    return render(request, 'base/error.html')