# Generated by Django 3.1.4 on 2021-02-01 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_user_city'),
        ('clinics', '0007_remove_clinic_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clinics', to='users.city'),
        ),
    ]