# Generated by Django 4.0.2 on 2022-04-08 21:58

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_remove_profile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True, default=''),
        ),
    ]