# Generated by Django 3.2 on 2022-02-27 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_alter_pricetime_mrp'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='pricing',
            field=models.IntegerField(default=0, help_text='Used to order stores based on pricing'),
        ),
    ]