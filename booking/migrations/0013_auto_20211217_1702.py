# Generated by Django 3.2 on 2021-12-17 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0012_auto_20211217_1629'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookingstatus',
            options={'verbose_name_plural': 'Booking Statuses'},
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bookings', to='booking.bookingstatus'),
        ),
    ]