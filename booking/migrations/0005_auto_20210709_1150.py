# Generated by Django 3.2 on 2021-07-09 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('store', '0013_auto_20210709_1106'),
        ('booking', '0004_alter_booking_vehicle_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='consumer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='accounts.consumer'),
        ),
        migrations.AlterField(
            model_name='review',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='store.store'),
        ),
    ]
