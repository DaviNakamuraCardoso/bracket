from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import User 

# Create your models here.
class Doctor(models.Model): 
    AREA_CHOICES = [
        ('Doctor', 'Doctor'), 
        ('Vet', 'Vet'), 
        ('Dentist', 'Dentist')
    ]
    number = models.IntegerField(unique=True) 
    degree = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    areas = ArrayField(models.CharField(max_length=64), null=True ,blank=True)
    


    def serialize(self): 
        return {
            'number': self.number, 
            'degree': self.degree, 
            'areas': ", ".join(self.areas)
        }
