# Generated by Django 3.2 on 2022-02-27 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_auto_20220227_1539'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='pricing',
            new_name='price_rating',
        ),
    ]
