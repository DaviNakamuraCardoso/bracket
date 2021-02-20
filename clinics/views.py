from django.shortcuts import render, reverse
from django.http import JsonResponse, HttpResponse
from clinics.models import Clinic
from base.models import Notification
from doctors.utils import get_doctor
from doctors.models import Doctor
from django.contrib.postgres.search import TrigramSimilarity
import json


def index(request):
    """ Return a page with all the top 10 clinics in the user city """
    clinics = Clinic.objects.all()[:10]

    if search := request.GET.get('search_query'):
        clinics = []
        results = Clinic.objects.annotate(
            similarity=TrigramSimilarity(
                'name', search)).all().order_by('-similarity')
        for clinic in results:
            if clinic not in clinics:
                clinics.append(clinic)

    return render(request, 'clinics/index.html', {
        'clinics': [clinic.serialize() for clinic in clinics]
    })


def profile(request, clinic_name):
    """ Return the clinic profile page """
    try:
        clinic = Clinic.objects.get(clinic_name=clinic_name)
    except Clinic.DoesNotExist:
        return HttpResponse('Error 404')


    context = {'clinic': clinic, 'senders': clinic.admin.notification_origins()}

    return render(request, 'clinics/profile.html', context)


def leave(request, clinic_name):
    clinic = Clinic.objects.get(clinic_name=clinic_name)
    doctor = request.user.doctor

    clinic.doctors.remove(doctor)
    return JsonResponse({"message": f"Succesfully left {clinic.name}", "url": reverse('clinics:join', args=(clinic.clinic_name, ))})


def join_clinic(request, clinic_name):
    """ Handles the invitation from the doctor """

    # Request must be PUT
    if request.method != "PUT":
        return JsonResponse({"message": "Method must be PUT"})

    # Get the essential data
    doctor = get_doctor(request=request)
    clinic = Clinic.objects.get(clinic_name=clinic_name)
    data = json.loads(request.body)

    # If the invite variable is false, delete the existing notification
    if not data['request']:
        notification = Notification.objects.get(
            origin=doctor.__str__(), user__name=clinic.admin.name
        )
        notification.delete()

        # Return a success message
        return JsonResponse({"message": "Join request cancelled succesfully", 'value': 'request', 'newInner': "Join"})

    # Generate a Notification for the clinic admin
    invite_text = f"Is asking to join {clinic.name}"
    invite_url = reverse('doctors:accept', args=(doctor.user.name, ))
    Notification.objects.create(
        clinic=clinic,
        user=clinic.admin,
        text=invite_text,
        url=invite_url,
        origin=doctor.__str__()
    )

    return JsonResponse({"message": "Request sent succesfully.", 'value': 'cancel', 'newInner': "Cancel Request"})


def doctor_in_clinics(request, doctor_name):
    # Definitions
    user = request.user
    doctor = Doctor.objects.get(user__name=doctor_name)

    # Checking for all clinics
    clinics = user.user_clinics.all()
    r = []

    #
    for clinic in clinics:
        if not doctor in clinic.doctors.all():
            r.append(clinic)
    clinics = [{'id': clinic.id, 'name': clinic.name} for clinic in r]
    context = {'clinics': clinics}

    return JsonResponse(context)
