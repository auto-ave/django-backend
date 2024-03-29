# Generated by Django 3.2 on 2022-03-03 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0008_vehicletype_position'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vehiclebrand',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='vehiclemodel',
            options={'ordering': ['model']},
        ),
        migrations.AddIndex(
            model_name='vehiclebrand',
            index=models.Index(fields=['name'], name='vehicle_veh_name_7cfb4b_idx'),
        ),
        migrations.AddIndex(
            model_name='vehiclemodel',
            index=models.Index(fields=['model'], name='vehicle_veh_model_5e1816_idx'),
        ),
    ]
