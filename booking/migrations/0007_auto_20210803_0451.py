# Generated by Django 3.2 on 2021-08-02 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_otp'),
        ('store', '0023_merge_0019_pricetime_description_0022_alter_event_bay'),
        ('vehicle', '0001_initial'),
        ('booking', '0006_slot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='price_time',
        ),
        migrations.AddField(
            model_name='booking',
            name='price_times',
            field=models.ManyToManyField(related_name='bookings', to='store.PriceTime'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booked_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bookings', to='accounts.consumer'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bookings', to='store.store'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='vehicle_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bookings', to='vehicle.vehicletype'),
        ),
    ]