# Generated by Django 3.2 on 2021-07-09 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_store_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='store_closing_time',
            new_name='closing_time',
        ),
        migrations.RenameField(
            model_name='store',
            old_name='store_opening_time',
            new_name='opening_time',
        ),
        migrations.RenameField(
            model_name='store',
            old_name='store_registration_number',
            new_name='registration_number',
        ),
        migrations.RenameField(
            model_name='store',
            old_name='store_registration_type',
            new_name='registration_type',
        ),
    ]