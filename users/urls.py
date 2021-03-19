from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Login / Logout
    path("login", views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),

    # Register and specifics
    path('register', views.register_view, name='register'),
    path('signup', views.signup_view, name='signup'),

    # Utils
    path('create', views.create_cities, name='create'),
#    path('eliminate', views.eliminate),
#    path('create_patients', views.create_patient),
#    path('create_doctors', views.create_doctor),

    # APIs
    path('location/<str:lat>/<str:lng>', views.location, name='location'),
    path('calendar/<int:year>/<int:month>', views.calendar, name='calendar'),
    path('find', views.find_location, name="find_location")
]
