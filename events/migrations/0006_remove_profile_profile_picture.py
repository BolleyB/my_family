# Generated by Django 5.0.3 on 2024-03-20 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_invitation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_picture',
        ),
    ]
