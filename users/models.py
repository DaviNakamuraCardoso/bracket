from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

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
        
        user = self._create_user(email, password, False, False, first_name, last_name, **extra_fields)
        return user 

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


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

    city = models.CharField(max_length=64, blank=True, null=True)

    # User type
    TYPES = [
        ('Doctor', 'Doctor'), 
        ('Patient', 'Patient'), 
        ('Clinic', 'Clinic')
    ]
    user_type = models.CharField(max_length=32, default="Patient", choices=TYPES)

    # Date fields 
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Clinic(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clinics")
    name = models.CharField(max_length=128)
    email = models.EmailField()
    city = models.CharField(max_length=64)


class Doctor(models.Model): 
    AREA_CHOICES = [
        ('Doctor', 'Doctor'), 
        ('Vet', 'Vet'), 
        ('Dentist', 'Dentist')
    ]
    number = models.IntegerField(unique=True) 
    degree = models.CharField(max_length=64)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    area = models.CharField(max_length=64, choices=AREA_CHOICES, blank=True, null=True)


class Patient(models.Model): 
    ALLERGIES = [
        ('Chem', 'Chem'), 
        ('Gluten', 'Gluten'), 
        ('Soap', 'Soap')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    # Basic 
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=3, decimal_places=2)

    allergies = ArrayField(models.CharField(max_length=64), size=20, null=True, blank=True)


    def __str__(self): 
        return f"{self.user.first_name} {self.user.last_name}'s ({self.user.name}) Medical Profile"


    def serialize(self): 
        return {
            'B.M.I.': round(self.get_bmi(), 2), 
            'weight': self.weight, 
            'height': self.height, 
            'allergies': ', '.join(self.allergies)
        }
    def get_bmi(self): 
        return self.weight / self.height ** 2 

    


    