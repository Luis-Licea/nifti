# Generated by Django 3.2 on 2022-03-29 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20220329_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='default.jpg', editable=False, upload_to='profile_pictures'),
        ),
    ]
