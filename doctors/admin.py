from django.contrib import admin
from doctors.models import Doctor, Area, Shift, Appointment


admin.site.register(Doctor)
admin.site.register(Area)
admin.site.register(Shift)
admin.site.register(Appointment)
