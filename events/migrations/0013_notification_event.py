# Generated by Django 5.0.3 on 2024-03-21 18:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_remove_notification_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.event'),
        ),
    ]