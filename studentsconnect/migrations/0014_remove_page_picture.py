# Generated by Django 5.0.1 on 2024-07-25 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentsconnect', '0013_page_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='picture',
        ),
    ]