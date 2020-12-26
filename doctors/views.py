from django.shortcuts import render, reverse 
from django.http import HttpResponse, HttpResponseRedirect
from doctors.models import Doctor 
from doctors.utils import get_doctor 
from clinics.utils import get_clinic, clinic_required  
from base.models import Notification 
# Create your views here.

def index(request): 
    return render(request, 'doctors/index.html')


def profile(request, name): 
    doctor = get_doctor(name)
    return render(request, 'doctors/profile.html', {
        'doctor': doctor, 
        'data': doctor.serialize()
    })


@clinic_required  
def invite(request, name): 
    doctor = get_doctor(name=name)
    clinic = get_clinic(request) 
    invite_text = f""
    Notification.objects.create(user=doctor.user, text=invite_text)
    return HttpResponseRedirect(reverse('base:index'))

    


