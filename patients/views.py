from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from users.models import Patient

# Create your views here.


@login_required 
def profile(request, name): 
    try: 
        patient = Patient.objects.get(user__name=name)
    except Patient.DoesNotExist: 
        return HttpResponse("Error 404")
    return render(request, 'patients/profile.html', {
        'patient': patient, 
        'data': patient.serialize()
    })
