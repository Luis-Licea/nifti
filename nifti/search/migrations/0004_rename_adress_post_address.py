# Generated by Django 4.0.2 on 2022-04-05 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_auto_20220329_1413'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='adress',
            new_name='address',
        ),
    ]
