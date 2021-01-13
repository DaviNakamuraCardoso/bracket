from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from users.data.cities import cities


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

    city = models.CharField(max_length=64, blank=True, null=True, choices=cities)

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

    


    # Date fields 
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def sorted_notifications(self): 
        return self.notifications.all().order_by('-timestamp')




    


    