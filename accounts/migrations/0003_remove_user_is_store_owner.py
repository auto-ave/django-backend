# Generated by Django 3.2 on 2021-08-19 04:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210815_1906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_store_owner',
        ),
    ]
