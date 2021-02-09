from django.db import models
from users.models import User, Day 
from clinics.models import Clinic
from patients.models import Patient
from users.data.time import sumtime, delta

# Create your models here.

class Area(models.Model): 
    area = models.CharField(max_length=128)

    def __str__(self): 
        return self.area


class Doctor(models.Model): 
    number = models.BigIntegerField() 
    degree = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    areas = models.ManyToManyField(Area, blank=True, related_name='doctors')
    clinics = models.ManyToManyField(Clinic, blank=True, related_name='doctors')
    
    def serialize(self): 
        return {
            'name': self.__str__(), 
            'number': self.number, 
            'degree': self.degree, 
            'areas': ", ".join([area.area for area in self.areas.all()]), 
            'email': self.user.email
        }

    def __str__(self): 
        return f"Dr. {self.user.first_name} {self.user.last_name}"
    
    def str(self): 
        return f"Dr. {self.user.first_name} {self.user.last_name}"
        

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
        return {
            'doctor': self.doctor.serialize(), 
            'clinic': self.clinic.serialize(), 
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
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    index = models.IntegerField(null=True, blank=True)
