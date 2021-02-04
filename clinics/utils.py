from clinics.models import Clinic 
from django.http import HttpResponseRedirect
from django.shortcuts import reverse 


def get_clinic(request): 
    user = request.user 

    clinic = None 
    if user.is_authenticated: 
        if user.is_clinic: 
            try: 
                clinic = Clinic.objects.get(user__email=user.email)
            except Clinic.DoesNotExist: 
                return HttpResponseRedirect(reverse('base:error'))
    
        return clinic 


def clinic_required(function):
    def inner(request, *args, **kwargs): 
        if not request.user.is_clinic: 
            return HttpResponseRedirect(reverse('base:error'))
        
        return function(request, *args, **kwargs)
            
    return inner 

    