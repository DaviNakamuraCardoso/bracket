# Generated by Django 3.1.4 on 2021-02-02 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0011_auto_20210201_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='break_end',
            field=models.TimeField(blank=True, null=True),
        ),
    ]