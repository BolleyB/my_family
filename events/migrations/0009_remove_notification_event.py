# Generated by Django 5.0.3 on 2024-03-21 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_notification_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='event',
        ),
    ]
