from users.models import User, City
from clinics.models import Clinic
from django.shortcuts import render, reverse 
from django.http import HttpResponseRedirect
from users.data import sorted_cities


def get_name(first, last): 

    """Gets first and last name and returns an username."""
    n = len(User.objects.filter(first_name=first, last_name=last))
    sufix = f".{(n)}" if n > 1 else ''
    sep = ''
    f = sep.join(first.split(" ")).lower()
    l = sep.join(last.split(" ")).lower()

    return f"{f}.{l}" + sufix


def get_clinic_name(request):
    """Get the name for the url."""
    name = request.POST['clinic_name'].split(' ')
    sep = ''
    base = sep.join(name).lower()
    l = len(Clinic.objects.filter(base_name=base))
    appendix = f".{l}" if l > 0 else ''
    

    return {'base': base, 'name': f"{base}{appendix}"}


def register(request, user_type): 
    """Handles the user register."""
    data = request.POST 

    # Create the basic user model 
    user = User.objects.create_user(
        password=data['password'], 
        user_type=user_type, 
        email=data['email'], 
        is_doctor=user_type=='doctor', 
        is_patient=user_type=='patient', 
        is_clinic=user_type=='clinic', 
        city=City.objects.get(pk=data['city'])
    )
    user.save()
    # For users that aren't clinics, set the first and last name
    if user_type != 'clinic': 
        first = data['first_name']
        last = data['last_name']
        
        user.name = get_name(first, last)
        user.first_name = first 
        user.last_name = last 

        user.save()
    
    return user 


