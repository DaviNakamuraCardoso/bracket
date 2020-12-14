from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import User, Clinic, Doctor
from patients.models import Patient 
from .forms import RegisterForm, LoginForm, DoctorForm, ClinicForm, PatientForm
from .utils import get_name 


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
            login(request, user)

            return HttpResponseRedirect(reverse('users:specific_register', args=(user.user_type.lower(), ))) 
    
    return render(request, 'users/register.html', {
        'form': form 
    })


def login_view(request): 
<<<<<<< HEAD
    """"""
=======
    """Handles the user login."""
>>>>>>> 9f213d5ff3d271ed3f7a214c5b38f4eec5cac771
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

@login_required
def specific_register(request, user_type):
    TYPES = {
        'clinic': {'form': ClinicForm, 'model': Clinic}, 
        'patient': {'form': PatientForm, 'model': Patient}, 
        'doctor': {'form': DoctorForm, 'model': Doctor}
    }
    if user_type not in TYPES.keys():
        return HttpResponse("No such type.")
    else: 
        # Get the specific form and model for the user type
        t = TYPES[user_type]
        form = t['form']()
        if request.method == "POST":

            # Starts the type object with the user set to the current user
            u = t['model'](user=request.user) 

            form = t['form'](request.POST, instance=u)

            if form.is_valid(): 
                form.save()
                return redirect('base:index')
            

    return render(request, 'users/specific.html', {
        'form': form, 
        'type': user_type
    })
