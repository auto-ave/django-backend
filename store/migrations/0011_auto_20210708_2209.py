# Generated by Django 3.2 on 2021-07-08 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_alter_booking_vehicle_type'),
        ('vehicle', '0001_initial'),
        ('store', '0010_alter_store_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bay',
            name='supported_vehicle_types',
            field=models.ManyToManyField(blank=True, to='vehicle.VehicleType'),
        ),
        migrations.AlterField(
            model_name='pricetime',
            name='vehicle_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='vehicle.vehicletype'),
        ),
        migrations.AlterField(
            model_name='store',
            name='supported_vehicle_types',
            field=models.ManyToManyField(blank=True, related_name='stores', to='vehicle.VehicleType'),
        ),
        migrations.DeleteModel(
            name='VehicleType',
        ),
    ]
