# Generated by Django 3.1.4 on 2020-12-18 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='base_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='clinic',
            name='clinic_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]