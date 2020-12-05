from django.db import models
from django.contrib.auth.models import AbstractUser 
import datetime 
# Create your models here.

class User(AbstractUser):
    # Every user has a trade number (ex: SSN in US, CPF in Brazil)
    trade_number = models.CharField(default="99999999999", max_length=20)
    birth = models.DateField(default=datetime.datetime.now)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"