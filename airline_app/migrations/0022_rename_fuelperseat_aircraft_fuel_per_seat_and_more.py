# Generated by Django 5.0.2 on 2024-04-17 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline_app', '0021_rename_fuelburn_aircraft_fuel_burn'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aircraft',
            old_name='fuelperseat',
            new_name='fuel_per_seat',
        ),
        migrations.AddField(
            model_name='aircraft',
            name='cruise_speed',
            field=models.PositiveSmallIntegerField(default=500),
        ),
        migrations.AddField(
            model_name='aircraft',
            name='pax_comfort',
            field=models.DecimalField(decimal_places=2, default=0.8, max_digits=3),
        ),
    ]
