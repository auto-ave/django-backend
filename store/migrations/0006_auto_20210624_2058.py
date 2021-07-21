# Generated by Django 3.2 on 2021-06-24 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20210624_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='vehicletype',
            name='model',
            field=models.CharField(choices=[('standard', 'Standard'), ('cruisers', 'Cruisers'), ('sports_bike', 'Sports Bike'), ('premium_bike', 'Premium Bike'), ('sedan', 'Sedan'), ('h_back', 'H-Back'), ('suv', 'SUV'), ('luxury', 'Luxury')], max_length=50, unique=True),
        ),
    ]
