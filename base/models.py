from django.db import models
from users.models import User
from clinics.models import Clinic
from doctors.models import Doctor
from base.time import strfdelta

# Create your models here.
class Notification(models.Model):
    object_id = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    origin = models.CharField(max_length=64, blank=True, null=True)
    text = models.CharField(max_length=128)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    read = models.BooleanField(default=False)
    url = models.URLField(max_length=64, blank=True, null=True)

    def serialize(self):
        return {
            'text': self.text,
            'url': self.url,
            'origin': self.origin,
            'time': self.time(),
            'object_id': self.object_id,
            'id': self.id
        }
    def __str__(self):
        return f"{self.user.name}: {self.text} on {self.timestamp}"

    def time(self):
        return strfdelta(timestamp=self.timestamp)


class Rate(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="ratings", blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="ratings", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings", blank=True, null=True)

    rate = models.FloatField()
    is_doctor_rating = models.BooleanField(default=False)
    comment = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.__str__()}'s rate"

    def time(self):
        return strfdelta(timestamp=self.timestamp)
