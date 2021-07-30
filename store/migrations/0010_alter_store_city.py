# Generated by Django 3.2 on 2021-07-08 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('store', '0009_alter_store_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='common.city'),
        ),
    ]