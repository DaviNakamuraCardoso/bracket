# Generated by Django 3.1.6 on 2021-03-15 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0014_clinic_allowed_raters'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='dashboard_version',
            field=models.BigIntegerField(default=0),
        ),
    ]