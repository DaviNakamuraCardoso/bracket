from django.urls import path 
from . import views 

app_name = 'users'

urlpatterns = [
    # Login / Logout
    path("login", views.login_view, name='login'), 
    path('logout', views.logout_view, name='logout'), 

    # Register and specifics
    path('register/patient', views.patient, name='patient'), 
    path('register/doctor', views.doctor, name='doctor'), 
    path('register/clinic', views.clinic, name='clinic'), 
    

    # Utils
    path('create', views.create_cities, name='create'), 
#    path('eliminate', views.eliminate), 
#    path('create_patients', views.create_patient), 
#    path('create_doctors', views.create_doctor), 

    # APIs 
    path('location/<str:lat>/<str:lng>', views.location, name='location')
]