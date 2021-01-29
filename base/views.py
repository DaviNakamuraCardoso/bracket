from django.shortcuts import render
from django.http import HttpResponseRedirect 
from clinics.models import Clinic
from users.forms import FORMS_CONTEXT
# Create your views here.

def index(request): 
    """Render all the clinics in the same city as the user."""
    local_context = {'user': request.user, 'clinics': Clinic.objects.all()}
    context = {**local_context, **FORMS_CONTEXT}
        
    return render(request, 'base/index.html', context=context)


def error(request): 
    """Return an error page for bad requests."""
    return render(request, 'base/error.html')