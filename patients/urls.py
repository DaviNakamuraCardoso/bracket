from django.urls import path
from . import views

app_name = 'patients'
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.profile, name='profile'),

    # APIS
    path("ratings/<int:appointment_id>", views.rate, name='rate'),
    path("ratings/<str:object>/<int:object_id>", views.all_rates, name='all_rates'),
    path("ratings/<str:object>/<int:object_id>/<int:page>", views.rates, name='rates'),
    path("rate/<str:object>", views.rate_redirect, name="rate_redirect")



]
