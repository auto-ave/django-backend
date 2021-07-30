# Generated by Django 3.2 on 2021-07-08 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('store', '0008_auto_20210708_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='city',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='common.city'),
        ),
    ]