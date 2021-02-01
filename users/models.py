from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import csv


# Create your models here.
class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        
        user = self._create_user(email, password, False, False, **extra_fields)
        return user 

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class City(models.Model): 
    # Name and state 
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=64)
    state_id = models.CharField(max_length=2)

    # Location 
    lat = models.FloatField()
    lng = models.FloatField()

    # Timezone
    timezone = models.CharField(max_length=32)
    

    def __str__(self): 
        return f"{self.city}, {self.state_id}"
    
    
    def serialize(self): 
        return {
            'city': self.city, 
            'id': self.id, 
            'state_id': self.state_id
        }


class User(AbstractBaseUser, PermissionsMixin):
    # Name and email  
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)

    # Permissions
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # User type
    TYPES = [
        ('Doctor', 'Doctor'), 
        ('Patient', 'Patient'), 
        ('Clinic', 'Clinic')
    ]
    user_type = models.CharField(max_length=32, default="Patient", choices=TYPES)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_clinic = models.BooleanField(default=False)

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='citizens', blank=True, null=True)


    # Date fields 
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def sorted_notifications(self): 
        return self.notifications.all().order_by('-timestamp')


    def notification_origins(self): 
        return [notification.origin for notification in self.notifications.all()]
    

class Day(models.Model): 
    day = models.CharField(max_length=32)

    def __str__(self): 
        return self.day 