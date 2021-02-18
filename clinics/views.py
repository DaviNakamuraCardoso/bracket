from django.shortcuts import render, reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from clinics.models import Clinic
from base.models import Notification
from doctors.utils import get_doctor
from clinics.utils import get_clinic
from django.contrib.postgres.search import TrigramSimilarity
import json

# Create your views here.

def index(request):
    clinics = Clinic.objects.all()

    if search := request.GET.get('search_query'):
        clinics = []
        results = Clinic.objects.annotate(similarity=TrigramSimilarity('name', search)).all().order_by('-similarity')
        for clinic in results:
            if clinic not in clinics:
                clinics.append(clinic)


    return render(request, 'clinics/index.html', {
        'clinics': [clinic.serialize() for clinic in clinics]
    })


def profile(request, clinic_name):
    try:
        clinic  = Clinic.objects.get(clinic_name=clinic_name)
    except Clinic.DoesNotExist:
        return HttpResponse('Error 404')

    context = {'clinic': clinic}

    return render(request, 'clinics/profile.html', context)


@csrf_exempt
def join_clinic(request, clinic_name):
    if request.method != "PUT":
        return JsonResponse({"message": "Method must be PUT"})

    doctor = get_doctor(request=request)
    clinic = Clinic.objects.get(clinic_name=clinic_name)
    data = json.loads(request.body)

    if not data['invite']:
        notification = Notification.objects.get(origin=doctor.str(), user__name=clinic.admin.name)
        notification.delete()

        return JsonResponse({"message": "Join request cancelled succesfully"})

    invite_text = f"Is asking to join {clinic.name}"
    invite_url = reverse('doctors:accept', args=(doctor.user.name, ))
    Notification.objects.create(user=clinic.admin, text=invite_text, url=invite_url, origin=doctor.str())

    return JsonResponse({"message": "Request sent succesfully."})
