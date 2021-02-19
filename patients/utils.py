from math import floor
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from background_task import background


@background(schedule=60)
def confirm_appointment(appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    user = appointment.user
    doctor = appointment.shift.doctor
    area = appointment.shift.area
    clinic = appointment.shift.clinic

    start, end = doctor.get_appointment_hour(appointment)

    message = f"{area.__str__()} appointment with {doctor.__str__()} scheduled for tomorrow at {start}."


    Notification.objects.create(
        user=user,
        clinic=clinic,
        text=message,
        origin=clinic.__str__()

    )


def patient(function):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_patient:
                return function(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('base:error'))

    return inner
