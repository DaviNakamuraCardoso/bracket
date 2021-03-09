from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('error/', views.error, name='error'),

    path("a/", views.areas, name="areas"),
    path('a/<str:area>', views.area, name="area"),

    # APIS
    path('<str:user_name>/notifications', views.all_notifications, name='notifications'), 
    path('<str:user_name>/notifications/<int:version>', views.notifications, name="version")
]
