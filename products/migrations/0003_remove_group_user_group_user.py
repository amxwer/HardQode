# Generated by Django 4.2.10 on 2024-02-29 15:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_remove_group_users_group_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='user',
        ),
        migrations.AddField(
            model_name='group',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
