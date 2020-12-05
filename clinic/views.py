from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserRegister, UserLogin 
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
    message = None
    if request.method == "POST": 
        form = UserLogin(request.POST) 
        if form.is_valid(): 
            if login_user(request, form.cleaned_data): 
                return HttpResponseRedirect(reverse('index'))
            else: 
                message = "Incorrect password/username/email"
    else: 
        form = UserLogin()
    return render(request, 'clinic/login.html', {
        'form': form, 
        'message': message
    })


def logout_view(request): 
    if request.user.is_authenticated: 
        logout(request, request.user)
        return HttpResponseRedirect(reverse('index'))