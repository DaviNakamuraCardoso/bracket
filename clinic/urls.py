from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.index, name='index'), 
    path('register', views.register, name="register"), 
    path('logout', views.logout_view, name="logout"), 
    path('login', views.login_view, name="login"), 
    path('logout', views.logout_view, name='logout'), 
    path('users/<username>', views.profile, name="profile")
]