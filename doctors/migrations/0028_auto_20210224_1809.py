# Generated by Django 3.1.6 on 2021-02-24 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0027_auto_20210224_0101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='area',
            name='symbol',
        ),
        migrations.AddField(
            model_name='area',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]