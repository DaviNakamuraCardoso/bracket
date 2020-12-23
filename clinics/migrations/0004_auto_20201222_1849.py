# Generated by Django 3.1.4 on 2020-12-22 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0003_auto_20201216_1957'),
        ('clinics', '0003_clinic_doctors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='doctors',
            field=models.ManyToManyField(blank=True, related_name='clinics', to='doctors.Doctor'),
        ),
    ]
