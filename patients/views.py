from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from base.models import Rate
from clinics.models import Clinic
from doctors.models import Appointment, Doctor
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
    if request.method != "POST":
        return JsonResponse({"message": "Method must be PUT."})

    data = json.loads(request.body)

    try:
        appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        return JsonResponse({"message": "You can only rate doctors after having an appointment with them."})

    if not appointment.checked:
        return JsonResponse({"message": "You can only rate appointments after it was checked by the doctor."})

    rate = Rate.objects.create(
        user=request.user,
        clinic=appointment.shift.clinic,
        doctor=appointment.shift.doctor,
        comment=data['body'],
        is_doctor_rating=data['is_doctor'],
        rate=data['rate']
    )

    if data['is_doctor']:
        appointment.shift.doctor.allowed_raters.remove(request.user)
    else:
        appointment.shift.clinic.allowed_raters.remove(request.user)


    return JsonResponse({"message": "Rating successfully sent", "rate": rate.serialize()})


@ajax_login_required
def rate_redirect(request, object):
    data = json.loads(request.body)
    appointment = Appointment.objects.get(pk=data['object_id'])
    model = appointment.shift.doctor if object == "doctors" else appointment.shift.clinic

    if data['accept']:
        return HttpResponseRedirect(reverse(f'{object}:ratings', args=(model.identifier())))

    return JsonResponse({"message": f"You can rate {model.__str__()} in its profile page."})


def all_rates(request, object, object_id):
    return HttpResponseRedirect(reverse('base:index'))


def rates(request, object, object_id, page):
    model = Doctor.objects.get(pk=object_id) if object == "doctors" else Clinic.object.get(pk=object_id)

    # Number of rates returned per request
    r = 5

    s, e = (r*page, r*(page+1))

    rates = model.ratings.filter(is_doctor_rating=object=="doctors").order_by('-timestamp')[s:e]
    context = {"rates": [rate.serialize() for rate in rates]}

    return JsonResponse(context)
