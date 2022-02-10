# Generated by Django 3.2 on 2022-02-05 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0027_alter_booking_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='max_booking_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='offer',
            name='min_booking_amount',
            field=models.IntegerField(default=0),
        ),
    ]