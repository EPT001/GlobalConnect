# Generated by Django 5.0.1 on 2024-07-04 19:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comhub', '0003_alter_question_date_created_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='likes',
            field=models.ManyToManyField(related_name='question_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
