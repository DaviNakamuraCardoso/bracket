# Generated by Django 3.1.6 on 2021-03-01 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0031_auto_20210301_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]