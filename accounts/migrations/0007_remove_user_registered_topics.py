# Generated by Django 3.2 on 2021-09-17 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_notificationtopic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='registered_topics',
        ),
    ]