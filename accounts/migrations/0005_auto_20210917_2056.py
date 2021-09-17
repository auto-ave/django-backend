# Generated by Django 3.2 on 2021-09-17 20:56

from django.db import migrations, models
import django_better_admin_arrayfield.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210917_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='fcm_tokens',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=230, null=True), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='user',
            name='registered_topics',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None),
        ),
    ]