from django.db import models
from users.models import User
from datetime import datetime, timezone
from base.time import intftimedelta, strfage 
import math

# Patient related models

class Allergy(models.Model):
    allergy = models.CharField(max_length=128)

    def __str__(self): 
        return self.allergy


class Condition(models.Model):
    condition = models.CharField(max_length=128)

    def __str__(self): 
        return self.condition 

class Medication(models.Model):
    medication = models.CharField(max_length=128)

    def __str__(self):
        return self.medication


class Patient(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    # Basic 
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=3, decimal_places=2)

    # Important medical information
    birth = models.DateTimeField(null=True, blank=True)
    allergies = models.ManyToManyField(Allergy, blank=True, related_name='allergic')
    conditions = models.ManyToManyField(Condition, blank=True, related_name='people')
    medications = models.ManyToManyField(Medication, blank=True, related_name='users')


    def __str__(self): 
        return f"{self.user.first_name} {self.user.last_name}'s ({self.user.name}) Medical Profile"


    def serialize(self): 
        return {
            'B.M.I.': round(self.get_bmi(), 2), 
            'weight': self.weight, 
            'height': self.height, 
            'birth': self.birth.strftime("%B %d, %Y"), 
            'age': self.get_age(), 
        }

    def get_bmi(self): 
        return self.weight / self.height ** 2 


    def get_age(self): 
        age = datetime.now(timezone.utc) - self.birth
        
        # Exact value of years, months and days
        al = intftimedelta(age)

        # Formatted string with the patient's age
        str_age = strfage(al['days'], al['months'], al['years'])

        return str_age  

