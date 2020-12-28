from django.http import HttpResponseRedirect 
from django.shortcuts import reverse 
from doctors.models import Doctor 


def get_doctor(name=None): 
    """Receive a name and returns a doctor object."""
    try: 
        doctor = Doctor.objects.get(user__name=name)
    except Doctor.DoesNotExist: 
        return HttpResponseRedirect(reverse('base:error'))
    return doctor 
    
    
def get_user_doctor(request): 
    """Receive the request and returns the current doctor."""
    if request.user.is_authenticated: 
        if request.user.is_doctor: 
            return request.user.doctor 

    
    return HttpResponseRedirect(reverse('base:error'))


def doctor(function): 
    def inner(request, *args, **kwargs): 
        if request.user.is_authenticated: 
            if request.user.is_patient: 
                return function(request, *args, **kwargs)
        

        return HttpResponseRedirect(reverse('base:error'))
    
    return inner 

