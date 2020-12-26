from django.shortcuts import render
from django.http import HttpResponse
from doctors.models import Doctor 
from doctors.utils import get_doctor 
from clinics.utils import get_clinic, check_clinic 
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


@check_clinic 
def invite(request, name): 
    doctor = get_doctor(name=name)
    clinic = get_clinic(request) 
    invite_text = f""
    Notification.objects.create(user=doctor.user, text=invite_text)
    return HttpResponseRedirect(reverse('base:index'))

    


