# Generated by Django 3.1.2 on 2020-12-05 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0007_user_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='age',
        ),
    ]
