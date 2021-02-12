from django.db import models
from users.models import User, City 
# Create your models here.

class Clinic(models.Model): 
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_clinics', blank=True, null=True)
    staff = models.ManyToManyField(User, blank=True, related_name='staff_clinics')


    # The actuall name  
    name = models.CharField(max_length=128)

    # Url name 
    clinic_name = models.CharField(max_length=128, null=True, blank=True)

    # Base to know how many equal urls are there
    base_name = models.CharField(max_length=128, null=True, blank=True)

    # Useful info 
    email = models.EmailField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='clinics', blank=True, null=True)
    address = models.CharField(max_length=256, null=True, blank=True)

    # Image 
    picture = models.ImageField(null=True, blank=True)


    def serialize(self): 
        return {
            'email': self.email, 
            'city': self.city.serialize(), 
            'doctors': [doctor.serialize() for doctor in self.doctors.all()], 
            'address': self.address
        }
    
    def __str__(self): 
        return f"{self.name}"

    def identifier(self): 
        return self.clinic_name

    def add_doctor(self, doctor): 
        self.doctors.add(doctor)
