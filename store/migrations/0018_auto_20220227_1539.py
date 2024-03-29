# Generated by Django 3.2 on 2022-02-27 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_store_pricing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='pricing',
            field=models.IntegerField(db_index=True, default=0, help_text='Used to order stores based on pricing'),
        ),
        migrations.AlterField(
            model_name='store',
            name='reputation',
            field=models.IntegerField(db_index=True, default=0, help_text='Used to order stores, higher reputation means higher priority'),
        ),
    ]
