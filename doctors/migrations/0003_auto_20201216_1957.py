# Generated by Django 3.1.4 on 2020-12-16 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0002_auto_20201215_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='number',
            field=models.IntegerField(),
        ),
    ]
