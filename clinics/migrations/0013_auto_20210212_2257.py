# Generated by Django 3.1.6 on 2021-02-12 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0012_clinic_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='picture',
            field=models.ImageField(default='clinic-default.png', upload_to=''),
        ),
    ]
