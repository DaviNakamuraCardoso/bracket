from django.contrib import admin
from .models import User, Doctor, Clinic 
from django.contrib.sites.models import Site
# Register your models here.


# Register the basic user models 
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Clinic)


