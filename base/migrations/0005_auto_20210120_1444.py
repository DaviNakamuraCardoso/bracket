# Generated by Django 3.1.4 on 2021-01-20 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_notification_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='origin',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
