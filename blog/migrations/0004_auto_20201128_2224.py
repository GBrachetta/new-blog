# Generated by Django 3.1.3 on 2020-11-28 22:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201128_2211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image_2',
        ),
        migrations.RemoveField(
            model_name='post',
            name='image_3',
        ),
        migrations.RemoveField(
            model_name='post',
            name='image_4',
        ),
        migrations.RemoveField(
            model_name='post',
            name='image_5',
        ),
        migrations.RemoveField(
            model_name='post',
            name='image_6',
        ),
        migrations.AlterField(
            model_name='post',
            name='image_1',
            field=models.ImageField(blank=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(['jpeg', 'jpg', 'png'])]),
        ),
    ]