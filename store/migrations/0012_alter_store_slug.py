# Generated by Django 3.2 on 2021-07-09 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20210708_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
