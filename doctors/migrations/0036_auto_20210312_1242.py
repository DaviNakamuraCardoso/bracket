# Generated by Django 3.1.6 on 2021-03-12 12:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doctors', '0035_doctor_allowed_raters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='allowed_raters',
            field=models.ManyToManyField(blank=True, related_name='doctor_rates', to=settings.AUTH_USER_MODEL),
        ),
    ]