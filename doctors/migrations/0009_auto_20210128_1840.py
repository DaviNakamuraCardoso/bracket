# Generated by Django 3.1.4 on 2021-01-28 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0008_doctor_areas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='number',
            field=models.BigIntegerField(),
        ),
    ]