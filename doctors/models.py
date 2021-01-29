from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import User 

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
    
    def serialize(self): 
        return {
            'number': self.number, 
            'degree': self.degree, 
            'areas': ", ".join(self.areas), 
            'email': self.user.email
        }

    def __str__(self): 
        return f"Dr. {self.user.first_name} {self.user.last_name}"
    
    def str(self): 
        return f"Dr. {self.user.first_name} {self.user.last_name}"
        
