from django.db import models
from users.models import User, City
from django.shortcuts import reverse


class Clinic(models.Model):
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_clinics',
        blank=True,
        null=True
    )
    staff = models.ManyToManyField(
        User,
        blank=True,
        related_name='staff_clinics'
    )

    # The actuall name
    name = models.CharField(max_length=128)

    # Url name
    clinic_name = models.CharField(max_length=128, null=True, blank=True)

    # Base to know how many equal urls are there
    base_name = models.CharField(max_length=128, null=True, blank=True)

    # Useful info
    email = models.EmailField()
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='clinics',
        blank=True, null=True
    )
    address = models.CharField(max_length=256, null=True, blank=True)

    # Image
    picture = models.ImageField(default='clinic-default.png')

    # Users allowed to rate
    allowed_raters = models.ManyToManyField(User, blank=True, related_name="clinic_rates")
    dashboard_version = models.BigIntegerField(default=1)

    def __str__(self):
        return f"{self.name}"

    def identifier(self):
        return self.clinic_name

    def serialize(self):
        return {
            'title': self.__str__(),
            'url': reverse('clinics:profile', args=(self.clinic_name, )),
            'name': self.clinic_name,
            'image': self.picture.url,
            'address': self.address,
            'status': 'OPEN',
            'info':  [self.email],
            'info_icon': 'mail',
            'info2': ['+1 3233-5555'],
            'info2_icon': 'phone',
            'rating': 5.0,
            'submodels':
                [doctor.basic_serialize() for doctor in self.doctors.all()]

        }

    def basic_serialize(self):
        return {
            'title': self.__str__(),
            'url': reverse('clinics:profile', args=(self.clinic_name, )),
            'image': self.picture.url,
            'id': self.id,
            'name': self.clinic_name
        }

    def areas(self):
        areas = []
        for shift in self.shifts.all():
            for area in shift.areas.all():
                if area not in areas:
                    areas.append(area)


        return areas

    def doctors_by_area(self):
        areas = {}
        for area in self.areas():
            areas[area] = []
            for doctor in self.doctors.all():
                for shift in doctor.shifts.all():
                    if shift.clinic == self and area in shift.areas.all():
                        areas[area].append(doctor)
                        break
        return areas
