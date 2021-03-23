from django.http import JsonResponse
from doctors.models import Doctor, Shift, Area
from doctors.utils import get_doctor


def schedule(request, name):
    doctor = get_doctor(name)

    context = [shift.serialize() for shift in sorted(doctor.shifts.all(), key=lambda shift:shift.day.id)]
    return JsonResponse(context, safe=False)
