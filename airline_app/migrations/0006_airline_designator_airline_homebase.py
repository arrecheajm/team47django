# Generated by Django 5.0.2 on 2024-04-15 01:56

import airline_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline_app', '0005_rename_fleets_fleet_airline_alter_fleet_airline_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='airline',
            name='designator',
            field=models.CharField(default=airline_app.models.random_airline_designator_generator, max_length=2),
        ),
        migrations.AddField(
            model_name='airline',
            name='homebase',
            field=models.CharField(default='DFW', max_length=3),
        ),
    ]
