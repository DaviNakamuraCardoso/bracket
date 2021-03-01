# Generated by Django 3.1.6 on 2021-02-23 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0025_area_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='picture',
        ),
        migrations.AddField(
            model_name='area',
            name='symbol',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]