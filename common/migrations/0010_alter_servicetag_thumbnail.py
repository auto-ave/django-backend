# Generated by Django 3.2 on 2022-01-04 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_alter_servicetag_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicetag',
            name='thumbnail',
            field=models.ImageField(upload_to='service_tags'),
        ),
    ]