# Generated by Django 3.2 on 2021-08-07 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storeimage',
            name='store',
        ),
        migrations.DeleteModel(
            name='ServiceImage',
        ),
        migrations.DeleteModel(
            name='StoreImage',
        ),
    ]
