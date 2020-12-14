from django.contrib import admin
from users.models import User, Doctor, Patient, Clinic 


# Register the basic user models 
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Clinic)


