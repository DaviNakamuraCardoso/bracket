from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate 
from .models import User 
from doctors.models import Doctor 
from patients.models import Patient 
from clinics.models import Clinic 
from .forms import RegisterForm, LoginForm, DoctorForm, ClinicForm, PatientForm
from .utils import get_name, get_clinic_name


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

            if user_type == 'clinic': 
                context = get_clinic_name(request)
                u.base_name = context[0]
                u.clinic_name = context[1] 
                request.user.is_clinic = True 
            elif user_type == 'doctor':  
                request.user.is_doctor = True 

            elif user_type == 'patient': 
                request.user.is_patient = True

            request.user.save()

            # Gets the form for the specific type of user 
            form = t['form'](request.POST, instance=u)


            if form.is_valid(): 
                form.save()
                return redirect('base:index')
                        

    return render(request, 'users/specific.html', {
        'form': form, 
        'type': user_type
    })
