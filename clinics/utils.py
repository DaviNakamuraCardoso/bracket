from clinics.models import Clinic 


def get_clinic(request): 
    user = request.user 

    clinic = None 
    if user.is_authenticated: 
        if user.is_clinic: 
            clinic = Clinic.objects.get(user__name=user.name)
    
    return clinic 

    