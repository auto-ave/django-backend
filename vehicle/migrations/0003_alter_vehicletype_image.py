# Generated by Django 3.2 on 2021-08-14 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0002_vehicletype_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicletype',
            name='image',
            field=models.URLField(default='https://d3to388m2zu1ph.cloudfront.net/media/questions/g916_1_1.png'),
        ),
    ]
