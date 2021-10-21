# Generated by Django 3.2 on 2021-09-25 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0005_vehicletype_wheel'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleBrand',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.URLField(default='https://d3to388m2zu1ph.cloudfront.net/media/questions/g916_1_1.png')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VehicleModel',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('model', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.URLField(default='https://d3to388m2zu1ph.cloudfront.net/media/questions/g916_1_1.png')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_models', to='vehicle.vehiclebrand')),
                ('vehicle_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_models', to='vehicle.vehicletype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]