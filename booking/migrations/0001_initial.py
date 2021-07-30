# Generated by Django 3.2 on 2021-05-03 09:10

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('booking_id', models.CharField(max_length=8)),
                ('status', models.PositiveIntegerField(choices=[(0, 'Started'), (1, 'Done'), (2, 'Error')])),
                ('status_changed_time', models.DateTimeField(default=datetime.datetime.now)),
                ('otp', models.CharField(max_length=4)),
                ('is_refunded', models.BooleanField(default=False)),
                ('booked_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.consumer')),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='store.event')),
                ('price_time', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.pricetime')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.store')),
                ('vehicle_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.vehicletype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_only_rating', models.BooleanField(default=True)),
                ('review_description', models.CharField(blank=True, max_length=250, null=True)),
                ('images', django.contrib.postgres.fields.ArrayField(base_field=models.ImageField(upload_to=''), blank=True, null=True, size=None)),
                ('rating', models.FloatField()),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='booking.booking')),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.consumer')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.store')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('refund_status', models.IntegerField(choices=[(0, 'Started'), (1, 'COMPLETED'), (2, 'Error')])),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='booking.booking')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_status', models.IntegerField()),
                ('transaction_id', models.CharField(max_length=10)),
                ('mode_of_payment', models.CharField(max_length=20)),
                ('amount', models.PositiveIntegerField()),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='booking.booking')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
