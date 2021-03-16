from django.db import models
from django.shortcuts import reverse
from users.models import User, Day
from clinics.models import Clinic
from patients.models import Patient
from users.data.time import sumtime, delta, format
from base.time import intftimedelta
from datetime import datetime, timedelta, date, time


class Area(models.Model):
    area = models.CharField(max_length=128)
    picture = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.area

    def serialize(self):
        return {
            "title": self.__str__(),
            "image": self.picture.url or '/images/general-practice_ApZO4A.png',
            "url": reverse('base:area', args=(self.__str__(), )),
            "submodels": [doctor.serialize() for doctor in self.doctors.all()]
        }


class Doctor(models.Model):
    number = models.BigIntegerField()
    degree = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    areas = models.ManyToManyField(Area, blank=True, related_name='doctors')
    clinics = models.ManyToManyField(Clinic, blank=True, related_name='doctors')

    allowed_raters = models.ManyToManyField(User, blank=True, related_name="doctor_rates")
    dashboard_version = models.BigIntegerField(default=1)

    def serialize(self):
        return {
            "image": self.user.picture.url,
            "title": self.__str__(),
            "name": self.user.name,
            "address": self.user.city.__str__(),
            "status": "working",
            "info": [self.degree],
            "info_icon": 'university',
            "info2": [clinic.basic_serialize() for clinic in self.clinics.all()],
            "info2_icon": 'clinic',
            "info3": self.areas.all(),
            "info3_icon": 'area',
            "rating": 5.0,
            "url": reverse('doctors:profile', args=(self.user.name, )),
            "submodels": [clinic.basic_serialize() for clinic in self.clinics.all()]
        }

    def basic_serialize(self):
        return {
            'title': self.__str__(),
            'image': self.user.picture.url,
            'url': reverse('doctors:profile', args=(self.user.name, )),
            'id': self.id 
        }

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

    def get_appointment_hour(self, appointment):
        shifts = self.shifts.filter(day=appointment.shift.day)
        hours = []
        for shift in shifts:
            hours += shift.get_appointments()

        hours.sort(key=lambda value:format(value[0]).total_seconds())
        start = hours[int(appointment.index)][0]
        end = hours[int(appointment.index)][1]

        return start, end


class Shift(models.Model):

    # Doctor and Day
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='shifts')
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='shifts')

    # Duration
    duration = models.DurationField(blank=True, null=True)
    start = models.TimeField(blank=True, null=True)
    end = models.TimeField(blank=True, null=True)
    break_time = models.TimeField(blank=True, null=True)
    break_end =  models.TimeField(blank=True, null=True)

    # Area and clinic
    areas = models.ManyToManyField(Area, blank=True, related_name='shifts')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, blank=True, related_name='shifts')


    def serialize(self):
        clinic_serialize = {**self.clinic.basic_serialize(), **{'address': f"{self.clinic.address}, {self.clinic.city.city}"}}
        doctor_serialize = self.doctor.basic_serialize()

        return {
            'doctor': doctor_serialize,
            'clinic': clinic_serialize,
            'areas': [area.area for area in self.areas.all()],
            'day': self.day.day,
            'id': self.id
        }

    def get_appointments(self):

        if self.break_time is not None and self.break_end is not None:
            shifts = (delta(self.start, self.break_time), delta(self.break_end, self.end))

            numbers = (round(shifts[0] / self.duration), round(shifts[1] / self.duration))

            appointments1 = [(sumtime(self.start, self.duration*i), sumtime(self.start, self.duration*(i+1))) for i in range(numbers[0])]
            appointments2 = [(sumtime(self.break_end, self.duration*i), sumtime(self.break_end, self.duration*(i+1))) for i in range(numbers[1])]
            appointments = appointments1 + appointments2

        else:

            tdelta = delta(self.start, self.end)
            numbers = round(tdelta / self.duration)

            appointments = [(sumtime(self.start, (self.duration*i)), sumtime(self.start, self.duration*(i+1))) for i in range(numbers)]

        return appointments


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    to = models.CharField(max_length=64, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_appointments', blank=True, null=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='shift_appointments')
    confirmed = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, blank=True, null=True)
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    index = models.IntegerField(null=True, blank=True)


    def serialize(self):
        return {
            "time": self.formatted_hours(),
            "patient": self.formatted_patient(),
            "status": self.status(),
            "delay": self.get_delay(),
            "area": self.area.__str__(),
            "id": self.id,
            "cancelled": self.cancelled,
            "checked": self.checked,
            "confirmed": self.confirmed,
            "index": self.index
        }

    def formatted_hours(self):
        s, e = self.shift.doctor.get_appointment_hour(self)
        return f"{':'.join(s.split(':')[:2])}-{':'.join(e.split(':')[:2])}"

    def formatted_patient(self):
        if self.to == self.user.__str__():
            return self.to

        return f"{self.to} (Re: {self.user.__str__()})"

    def status(self):

        if self.checked:
            return "checked"


        if self.cancelled:
            return "cancelled"

        if self.confirmed:
            return "confirmed"

        return "not confirmed"

    def get_delay(self):
        n = datetime.now()
        now = n - datetime(year=n.year, month=n.month, day=n.day, hour=self.user.timezone_delay())
        s, e = self.shift.doctor.get_appointment_hour(self)
        e = format(e)


        if (now-e).total_seconds() <= 0:
            return "-", "empty"

        r = intftimedelta(timedelta=(now-e))
        hours = r['hours']
        minutes = r['minutes']

        if hours <= 0:
            return f"{minutes}min", "minutes"

        return f"{hours}h {'{:02}'.format(minutes)}min", "hours"
