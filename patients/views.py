from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from patients.models import Patient
from django.contrib.postgres.search import TrigramSimilarity
import json
# Create your views here.


def index(request):
    patients = Patient.objects.all()[:10]
    if search := request.GET.get('search_query'):

        patients = Patient.objects.annotate(similarity=TrigramSimilarity('user__name', search)).all().order_by('-similarity')


    return render(request, 'patients/index.html', {
        'patients': patients
    })
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
