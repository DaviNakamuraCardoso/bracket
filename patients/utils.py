from math import floor 
from django.http import HttpResponseRedirect
from django.shortcuts import reverse  



def patient(function): 
    def inner(request, *args, **kwargs): 
        if request.user.is_authenticated: 
            if request.user.is_patient: 
                return function(request, *args, **kwargs)
        
        return HttpResponseRedirect(reverse('base:error'))
    
    return inner 


   