# Generated by Django 5.0.3 on 2024-03-21 18:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_profile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='event',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='events.event'),
            preserve_default=False,
        ),
    ]
