from django.contrib import admin
from .models import Patient, Condition, Allergy, Medication

# Register your models here.
admin.site.register(Patient)
admin.site.register(Condition)
admin.site.register(Allergy)
admin.site.register(Medication)
        