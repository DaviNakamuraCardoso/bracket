# Generated by Django 3.1.4 on 2021-01-28 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allergy', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medication', models.CharField(max_length=64)),
            ],
        ),
    ]