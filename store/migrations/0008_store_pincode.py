# Generated by Django 3.2 on 2021-08-10 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20210807_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='pincode',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
