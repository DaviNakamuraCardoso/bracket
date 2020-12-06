from django.db import models
from django.contrib.auth.models import AbstractUser 
from datetime import datetime as date 

# Create your models here.
class User(AbstractUser):
    # Every user has a trade number (ex: SSN in US, CPF in Brazil)
    trade_number = models.CharField(default="99999999999", max_length=20)
    birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    
    def get_age(self): 
        age = date.now().year - self.birth.year
        return age


class Statistics(models.Model):
    # Each user has its own statistics 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="statistics")

    # Basics 
    weight = models.FloatField()
    height = models.FloatField()

    def get_bmi(self):
        bmi = self.weight / self.height ** 2

        return bmi 

    


