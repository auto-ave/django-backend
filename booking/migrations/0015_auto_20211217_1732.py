# Generated by Django 3.2 on 2021-12-17 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0014_cancellationrequest_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='status',
            new_name='booking_status',
        ),
        migrations.RenameField(
            model_name='cancellationrequest',
            old_name='status',
            new_name='cancellation_status',
        ),
    ]