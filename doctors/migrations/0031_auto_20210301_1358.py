# Generated by Django 3.1.6 on 2021-03-01 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0030_auto_20210301_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='picture',
            field=models.ImageField(default='general-practice.png', upload_to=''),
        ),
    ]