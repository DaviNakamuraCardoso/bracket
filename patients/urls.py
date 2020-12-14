from django.urls import path 
from . import views 

app_name = 'patients'
urlpatterns = [
    path("<str:name>", views.profile, name='profile')


]