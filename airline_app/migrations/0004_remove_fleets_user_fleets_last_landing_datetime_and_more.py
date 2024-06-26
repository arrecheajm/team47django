# Generated by Django 5.0.2 on 2024-04-14 21:29

import airline_app.models
import datetime
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline_app', '0003_fleets'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fleets',
            name='user',
        ),
        migrations.AddField(
            model_name='fleets',
            name='last_landing_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='fleets',
            name='location',
            field=models.CharField(default='', max_length=3),
        ),
        migrations.AddField(
            model_name='fleets',
            name='manufacture_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='fleets',
            name='registration',
            field=models.CharField(default=airline_app.models.random_aircraft_registration_generator, max_length=8),
        ),
        migrations.AlterField(
            model_name='fleets',
            name='operating_hours',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16),
        ),
        migrations.CreateModel(
            name='Airlines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Acme Airlines', max_length=32)),
                ('revenue', models.DecimalField(decimal_places=2, max_digits=32)),
                ('costs', models.DecimalField(decimal_places=2, max_digits=32)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='fleets',
            name='airline',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='airline_app.airlines'),
        ),
    ]
