from . import views 
from django.urls import path 

app_name = 'clinics'

urlpatterns = [
    path('', views.index, name='index'), 
    path('<str:clinic_name>', views.profile, name='profile'), 
    path('<str:clinic_name>/invitation', views.invitation, name='invitation') 

]