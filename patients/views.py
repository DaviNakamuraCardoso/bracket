from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from patients.models import Patient
from users.decorators import ajax_login_required
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


@ajax_login_required
def rate(request, appointment_id):
    if request.method != "PUT":
        return JsonResponse({"message": "Method must be PUT."})

    data = json.loads(request.body)

    try:
        appointment = Appointment.objects.get(pk=data['appointment_id'])
    except Appointment.DoesNotExist:
        return JsonResponse({"message": "You can only rate doctors after having an appointment with them."})

    if not appointment.checked:
        return JsonResponse({"message": "You can only rate appointments after it was checked by the doctor them."})

    Rate.objects.create(
        user=request.user,
        clinic=Clinic.objects.get(pk=data['id']) if not data['is_doctor'] else None,
        doctor=Doctor.objects.get(pk=data['id']) if data['is_doctor'] else None,
        comment=data['comment'],
        rating=data['rate']
    )

    return JsonResponse({"message": "Rating successfully sent"})


@ajax_login_required
def rate_redirect(request):
    data = json.loads(request.body)
    appointment = Appointment.objects.get(pk=data['object_id'])
    doctor_name = appointment.shift.doctor.user.name
    appointment.delete()

    if data['accept']:
        return HttpResponseRedirect(reverse('doctors:ratings', args=(doctor_name)))

    return JsonResponse({"message": ""})
