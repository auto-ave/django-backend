# Generated by Django 3.2 on 2021-07-24 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_rename_slot_interval_store_slot_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bay',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bays', to='store.store'),
        ),
    ]