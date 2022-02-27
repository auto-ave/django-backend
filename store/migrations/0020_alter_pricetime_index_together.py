# Generated by Django 3.2 on 2022-02-27 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0017_auto_20220225_1616'),
        ('vehicle', '0008_vehicletype_position'),
        ('store', '0019_rename_pricing_store_price_rating'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='pricetime',
            index_together={('service', 'vehicle_type', 'is_offer')},
        ),
    ]