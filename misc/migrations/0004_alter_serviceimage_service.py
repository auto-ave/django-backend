# Generated by Django 3.2 on 2021-07-20 07:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_service'),
        ('misc', '0003_serviceimage_storeimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceimage',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='common.service'),
        ),
    ]