# Generated by Django 3.2 on 2022-01-27 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0024_booking_is_multi_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]