# Generated by Django 5.0.2 on 2024-04-16 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline_app', '0018_alter_airport_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='airport',
            name='dst',
            field=models.BooleanField(default=False),
        ),
    ]
