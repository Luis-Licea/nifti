# Generated by Django 4.0.2 on 2022-04-01 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20220329_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='description',
        ),
    ]