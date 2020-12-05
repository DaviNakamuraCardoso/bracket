from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.db import IntegrityError 
from .forms import UserRegister, UserLogin 
from .models import User 
from .utils import register_user, login_user

# Create your views here.
def index(request): 
    return render(request, 'clinic/index.html')


def register(request): 
    if request.method == 'POST': 
        form = UserRegister(request.POST)

        if form.is_valid(): 
            if register_user(request, form.cleaned_data):
                 
                return HttpResponseRedirect(reverse('index'))
        
    else: 
        form = UserRegister() 

    return render(request, 'clinic/register.html', {
        'form': form 
    })
    

def login_view(request):

    if request.method == "POST": 
        form = UserLogin(request.POST) 
        if form.is_valid(): 

            data = form.cleaned_data
            username = data['key']
            password = data['password']

            user = authenticate(request=request, username=username, password=password)

            if user is not None: 
                login(request=request, user=user)
                return HttpResponseRedirect(reverse('index'))
            else: 
                return render(request, 'clinic/login.html', {
                    'form': form, 
                    'message': 'Incorrect password/email.' 
                })
                
            
    else: 
        form = UserLogin()
    return render(request, 'clinic/login.html', {
        'form': form 
    })


def logout_view(request): 
    # Allows logout only for authenticated users 
    if request.user.is_authenticated: 
        logout(request)
        return HttpResponseRedirect(reverse('index'))


def profile(request, username): 
    try: 
        user = User.objects.get(username=username)
        stats = {
            "age":user.get_age(), 
            "weight": 19
        }
    except IntegrityError: 
        return HttpResponseRedirect(reverse('index'))
    
    return render(request, 'clinic/profile.html', {
        'profile': user, 
        'stats': stats
    })
