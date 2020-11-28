# Generated by Django 3.1.3 on 2020-11-28 22:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(['jpeg', 'jpg', 'png'])]),
        ),
    ]
