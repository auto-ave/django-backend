# Generated by Django 3.2 on 2021-09-21 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_notificationtopic_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='fcm_tokens',
        ),
    ]
