# Generated by Django 5.0.2 on 2024-04-24 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline_app', '0095_fleet_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fleet',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this fleet aircraft should be treated as active.Uncheck instead of deleting fleet aircarft.', verbose_name='Active'),
        ),
    ]
