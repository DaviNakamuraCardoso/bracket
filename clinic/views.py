from django.shortcuts import render, reverse
from django.http import HttpResponse 
from .forms import UserRegister
from .utils import register_user
# Create your views here.

def index(request):
    return HttpResponse("Hello, bracket!")
    

def register(request):
    if request.method == 'POST':
        form = UserRegister()

        if form.is_valid():

            if register_user(form.cleaned_data):

                return HttpResponseRedirect(reverse('index'))
            else: 
                HttpResponse("Lixo")
            
    else: 
        form = UserRegister(request.POST)

        

    return render(request, "clinic/register.html", {
            'form': form
        })
    
       


        

    return render(request, "register.html")



