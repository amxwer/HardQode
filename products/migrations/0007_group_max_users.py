# Generated by Django 4.2.10 on 2024-02-29 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_rename_user_group_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='max_users',
            field=models.PositiveIntegerField(default=5),
        ),
    ]
