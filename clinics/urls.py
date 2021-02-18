from . import views
from django.urls import path

app_name = 'clinics'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:clinic_name>', views.profile, name='profile'),
    path('<str:clinic_name>/join', views.join_clinic, name='join'),

    # APIs
    path('doctor/<str:doctor_name>', views.doctor_in_clinics, name="doctor_in_clinics"),
    path("<str:clinic_name>/leave", views.leave, name="leave")
]
