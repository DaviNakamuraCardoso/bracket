from django.contrib import admin
from doctors.models import Doctor, Area, Shift

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Area)
admin.site.register(Shift)