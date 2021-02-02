from django.db import models
from users.models import User, Day 
from clinics.models import Clinic


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
