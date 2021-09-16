# Generated by Django 3.2 on 2021-09-17 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_store_slot_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='merchant_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='pincode',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
