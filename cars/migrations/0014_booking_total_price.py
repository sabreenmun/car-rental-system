# Generated by Django 5.1.6 on 2025-03-19 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0013_car_available_dates'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
