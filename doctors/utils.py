from django.http import HttpResponseRedirect 
from django.shortcuts import reverse 
from doctors.models import Doctor 


def get_doctor(name): 
    """Receive a name and returns a doctor object."""
    try: 
        doctor = Doctor.objects.get(user__name=name)
    except Doctor.DoesNotExist: 
        return HttpResponseRedirect(reverse('base:error'))
    
    return doctor 


