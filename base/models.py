from django.db import models
from users.models import User 


# Create your models here.
class Notification(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    text = models.CharField(max_length=128)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self): 
        return f"{self.user.name}: {self.text} on {self.timestamp}"
    
