from django.urls import path 
from . import views 


app_name = 'doctors'

urlpatterns = [
    path("", views.index, name="index"), 
    path("<str:name>", views.profile, name="profile"), 
    path("<str:name>/invite", views.invite, name="invite")

]