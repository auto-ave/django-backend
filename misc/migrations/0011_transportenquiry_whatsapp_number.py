# Generated by Django 3.2 on 2022-06-13 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0010_auto_20220613_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='transportenquiry',
            name='whatsapp_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
