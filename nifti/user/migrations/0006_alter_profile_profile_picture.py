# Generated by Django 3.2 on 2022-03-29 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20220329_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='profile_pictures/default.jpg', editable=False, upload_to='profile_pictures'),
        ),
    ]
