# Generated by Django 3.1.4 on 2021-02-09 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0019_appointment_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='doctors.area'),
        ),
    ]
