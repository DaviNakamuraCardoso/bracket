from clinic.models import User 
from django.db import models 

class Patient(User): 
    weight = models.IntegerField(null=True, blank=True)
    