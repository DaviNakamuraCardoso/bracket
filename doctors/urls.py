from django.urls import path
from . import views


app_name = 'doctors'

urlpatterns = [
    path("", views.index, name="index"),

    path("<str:name>", views.profile, name="profile"),
    path("<str:name>/about", views.profile, name="about"),
    path("<str:name>/ratings", views.profile, name="ratings"),
    path("<str:name>/add", views.add, name="add"),
    path("<str:name>/accept", views.accept, name="accept"),
    path("<str:name>/schedule", views.schedule_view, name="schedule"),
    path("<str:name>/days/<str:clinic>/<str:area>", views.schedule_days, name="days"),
    path("<str:name>/appointment", views.new_appointment, name="new-appointment"),


    path("<str:name>/<int:year>/<int:month>/<int:day>", views.day_planner, name="day-planner"),
    path("<str:name>/<int:year>/<int:month>/<int:day>/<int:index>", views.appointment_planner, name="appointment-planner"),
    path("<str:name>/<int:year>/<int:month>/<int:day>/<int:index>/confirm", views.confirm, name="confirm"),
    path("appointments/<int:appointment_id>", views.check, name="check")


]
