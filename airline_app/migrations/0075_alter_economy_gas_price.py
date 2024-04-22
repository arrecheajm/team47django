# Generated by Django 5.0.2 on 2024-04-21 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline_app', '0074_alter_flight_is_canceled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='economy',
            name='gas_price',
            field=models.DecimalField(decimal_places=6, default=1.1, max_digits=10, verbose_name='Gas Price ($/lb)'),
        ),
    ]