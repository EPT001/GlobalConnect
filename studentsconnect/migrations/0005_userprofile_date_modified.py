# Generated by Django 5.0.1 on 2024-07-08 17:19

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentsconnect', '0004_userprofile_follows'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name=django.contrib.auth.models.User),
        ),
    ]
