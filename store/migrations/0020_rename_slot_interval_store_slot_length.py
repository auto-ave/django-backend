# Generated by Django 3.2 on 2021-07-23 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_store_slot_interval'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='slot_interval',
            new_name='slot_length',
        ),
    ]
