# Generated by Django 5.0.2 on 2024-04-17 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline_app', '0022_rename_fuelperseat_aircraft_fuel_per_seat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aircraft',
            name='price_millions',
            field=models.SmallIntegerField(default=100),
        ),
    ]
