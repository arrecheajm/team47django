# Generated by Django 5.0.2 on 2024-04-19 23:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline_app', '0065_alter_flight_aircraft'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='aircraft',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airline_app.fleet'),
        ),
    ]
