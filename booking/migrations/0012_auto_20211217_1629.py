# Generated by Django 3.2 on 2021-12-17 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0011_cancellationrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'NOT_PAID'), (10, 'PAYMENT_DONE'), (20, 'PAYMENT_FAILED'), (30, 'NOT_ATTENDED'), (40, 'SERVICE_STARTED'), (50, 'SERVICE_COMPLETED'), (60, 'CANCELLATION_REQUEST_SUBMITTED'), (70, 'CANCELLED')]),
        ),
    ]