# Generated by Django 3.2 on 2021-07-08 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0001_initial'),
        ('booking', '0003_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='vehicle_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vehicle.vehicletype'),
        ),
    ]
