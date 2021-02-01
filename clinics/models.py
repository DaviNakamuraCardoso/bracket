from django.db import models
from users.models import User, City 
from doctors.models import Doctor 
# Create your models here.

class Clinic(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The actuall name  
    name = models.CharField(max_length=128)

    # Url name 
    clinic_name = models.CharField(max_length=128, null=True, blank=True)

    # Base to know how many equal urls are there
    base_name = models.CharField(max_length=128, null=True, blank=True)

    # Useful info 
    email = models.EmailField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='clinics', blank=True, null=True)

    doctors = models.ManyToManyField(Doctor, blank=True, related_name='clinics')

    def serialize(self): 
        return {
            'email': self.email, 
            'city': self.city, 
            'doctors': [doctor for doctor in self.doctors.all()]
        }
    
    def __str__(self): 
        return f"{self.name}"

    def add_doctor(self, doctor): 
        self.doctors.add(doctor)
