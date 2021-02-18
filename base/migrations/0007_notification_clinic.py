# Generated by Django 3.1.6 on 2021-02-18 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0013_auto_20210212_2257'),
        ('base', '0006_notification_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='clinic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clinic_notifications', to='clinics.clinic'),
        ),
    ]
