# Generated by Django 5.0.2 on 2024-04-23 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline_app', '0083_alter_flight_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlightCostModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_hours_year', models.FloatField(default=800.0, verbose_name='Flight Hours/Year')),
                ('captain_salary', models.FloatField(default=200000.0, verbose_name="Captain's Salary $")),
                ('first_officer_salary', models.FloatField(default=110000.0, verbose_name="First Officer's Salary $")),
                ('flight_attendant_salary', models.FloatField(default=55000.0, verbose_name="Flight Attendant's Salary $")),
            ],
        ),
        migrations.AddField(
            model_name='flight',
            name='captains_onboard',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='flight',
            name='first_officers_onboard',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='flight',
            name='flight_attendants',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
