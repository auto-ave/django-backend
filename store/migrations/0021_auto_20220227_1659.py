# Generated by Django 3.2 on 2022-02-27 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_alter_pricetime_index_together'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='pricetime',
            index_together=set(),
        ),
        migrations.AddIndex(
            model_name='pricetime',
            index=models.Index(fields=['service', 'vehicle_type', 'is_offer'], name='store_price_service_83efca_idx'),
        ),
    ]
