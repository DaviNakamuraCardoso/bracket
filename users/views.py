from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse 
from .forms import RegisterForm, LoginForm

# Create your views here.
def register_view(request): 
    form = RegisterForm() 
    if request.method == "POST": 
        form = RegisterForm(request.POST)
        if form.is_valid(): 
            form.save()
            user = User.objects.get(email=form.cleaned_data['email'])
            user.name = get_name(form.cleaned_data['first_name'], form.cleaned_data['last_name'])

            user.save()
            login(request, user)
            return redirect('clinic:index') 
    
    return render(request, 'users/register.html', {
        'form': form
    })


def login_view(request): 
    form = LoginForm()
    if request.method == "POST": 
        form = LoginForm(request.POST)
        if form.is_valid(): 
            username = form.cleaned_data['username'] 
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None: 
                login(request, user)
                return redirect('clinic:index')
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


def logout_view(request): 
    if request.user.is_authenticated: 
        logout(request)
    return redirect('clinic:index')


def get_name(first, last): 
    n = len(User.objects.filter(first_name=first, last_name=last))
    sep = ''
    f = sep.join(first.split(" ")).lower()
    l = sep.join(last.split(" ")).lower()

    return f"{f}.{l}.{n+1}"
