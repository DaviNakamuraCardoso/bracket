# Generated by Django 3.1.6 on 2021-03-15 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0015_clinic_dashboard_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='dashboard_version',
            field=models.BigIntegerField(default=1),
        ),
    ]
