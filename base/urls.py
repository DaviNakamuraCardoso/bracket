from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('error/', views.error, name='error'),

    path("a/", views.areas, name="areas"), 
    path('a/<str:area>', views.area, name="area"),
    # APIS
    path('<str:user_name>/notifications', views.notifications, name='notifications')
]
