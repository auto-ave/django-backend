# Generated by Django 3.2 on 2021-10-21 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='upcoming',
            field=models.BooleanField(default=False),
        ),
    ]
