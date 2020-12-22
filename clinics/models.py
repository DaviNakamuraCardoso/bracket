from django.db import models
from users.models import User 


# Create your models here.
class Clinic(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clinics")
    name = models.CharField(max_length=128)
    clinic_name = models.CharField(max_length=128, null=True, blank=True)
    base_name = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField()
    city = models.CharField(max_length=64)


    def serialize(self): 
        return {
            'owner': f"{self.user.first_name} {self.user.last_name}", 
            'email': self.email, 
            'city': self.city
        }



