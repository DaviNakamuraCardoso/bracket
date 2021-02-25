from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from background_task import background
from datetime import datetime, timedelta
from doctors.models import Appointment
from base.models import Notification
from math import floor


def confirmation(appointment):
    start, end = appointment.shift.doctor.get_appointment_hour(appointment)
    time = datetime.strptime(f"{start} {appointment.day}/{appointment.month}/{appointment.year}", "%H:%M:%S %d/%m/%Y")
    delta = (time + timedelta(hours=appointment.user.timezone_delay())) - (datetime.now() + timedelta(days=1))
    confirm_appointment(appointment.id, schedule=delta)


@background
def confirm_appointment(appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    user = appointment.user
    doctor = appointment.shift.doctor
    area = appointment.area
    clinic = appointment.shift.clinic

    start, end = doctor.get_appointment_hour(appointment)

    message = f"{area.__str__()} appointment with {doctor.__str__()} scheduled for tomorrow at {start}."


    Notification.objects.create(
        user=user,
        object_id=appointment.id,
        text=message,
        origin=clinic.__str__(),
        url=reverse('doctors:confirm', args=(doctor.user.name, appointment.year, appointment.month, appointment.day, appointment.index, ))


    )


def patient(function):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_patient:
                return function(request, *args, **kwargs)

        return HttpResponseRedirect(reverse('base:error'))

    return inner
