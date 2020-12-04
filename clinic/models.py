from django.db import models
from django.contrib.auth.models import AbstractUser 
import datetime
# Create your models here.

class User(AbstractUser):
    birth = models.DateTimeField(auto_now_add=True)
    trade_number = models.IntegerField(default=99999999999)
    foo = models.CharField(default="I hate Django", max_length=64)


    