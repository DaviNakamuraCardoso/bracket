from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate 
from .models import User, City
from doctors.models import Doctor 
from patients.models import Patient 
from clinics.models import Clinic 
from .forms import RegisterForm, LoginForm, DoctorForm, ClinicForm, PatientForm
from .utils import get_name, get_clinic_name
from users.data.cities import cities


# Create your views here.
def register_view(request): 
    """"""
    form = RegisterForm() 

    if request.method == "POST": 
        form = RegisterForm(request.POST)


        if form.is_valid(): 
            form.save()
            user = User.objects.get(email=form.cleaned_data['email'])
            # Automatically defines an username
            user.name = get_name(form.cleaned_data['first_name'], form.cleaned_data['last_name'])

            user.save()

            return HttpResponseRedirect(reverse(f'users:{user.type.lower()}')) 
    
    return render(request, 'users/register.html', {
        'form': form 
    })

def patient(request): 
    pass 

def doctor(request): 
    pass 

def clinic(request): 
    pass


def login_view(request): 
    """Handles the user login."""
    form = LoginForm()
    if request.method == "POST": 
        form = LoginForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None: 
                login(request, user)
                return redirect('base:index')
            else: 
                return render(request, 'users/login.html', {
                    'form': form, 
                    'message': 'Incorrect username/password'
                })
        else: 
            form = LoginForm()
    return render(request, 'users/login.html', {
        'form': form
    })

@login_required
def logout_view(request): 
    if request.user.is_authenticated: 
        logout(request)
    return redirect('base:index')



def create_cities(request): 
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('base:error'))
    
    for city in cities: 
        City.objects.create(
            city=city[0], 
            state=city[3], 
            state_id=city[2], 
            lat=float(city[6]), 
            lng=float(city[7])
        )

    return HttpResponseRedirect(reverse('base:index')) 

    