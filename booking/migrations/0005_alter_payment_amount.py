# Generated by Django 3.2 on 2021-08-20 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_payment_payment_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
