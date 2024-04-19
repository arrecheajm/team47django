# Generated by Django 5.0.2 on 2024-04-17 17:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline_app', '0030_flight_aircraft'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='aircraft',
            field=models.ForeignKey(limit_choices_to={'airline': models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline_app.airline')}, on_delete=django.db.models.deletion.CASCADE, to='airline_app.fleet'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='airline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline_app.airline'),
        ),
    ]
