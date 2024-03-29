# Generated by Django 3.2 on 2022-06-05 20:51

import custom_admin_arrayfield.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0006_sendgridemailevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sendgridemailevent',
            name='category',
            field=custom_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200, null=True), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='sendgridemailevent',
            name='email',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sendgridemailevent',
            name='event',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sendgridemailevent',
            name='ip',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sendgridemailevent',
            name='reason',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sendgridemailevent',
            name='response',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sendgridemailevent',
            name='sgEventId',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sendgridemailevent',
            name='sgMessageId',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='sendgridemailevent',
            name='smtpId',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='sendgridemailevent',
            name='status',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sendgridemailevent',
            name='url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sendgridemailevent',
            name='useragent',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
