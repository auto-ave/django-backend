# Generated by Django 3.2 on 2022-01-06 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_alter_servicetag_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicetag',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]
