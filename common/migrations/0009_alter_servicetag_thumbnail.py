# Generated by Django 3.2 on 2022-01-03 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_auto_20220103_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicetag',
            name='thumbnail',
            field=models.URLField(default='https://google.com'),
            preserve_default=False,
        ),
    ]
