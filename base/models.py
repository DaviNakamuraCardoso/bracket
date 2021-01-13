from django.db import models
from users.models import User 
from base.time import strfdelta 

# Create your models here.
class Notification(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    origin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', blank=True, null=True)
    text = models.CharField(max_length=128)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self): 
        return f"{self.user.name}: {self.text} on {self.timestamp}"
    
    def time(self):
        return strfdelta(timestamp=self.timestamp) 
    
        
