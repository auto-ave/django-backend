# Generated by Django 3.2 on 2021-08-25 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0003_auto_20210825_2317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wheel',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Two Wheeler, Three Wheeler, Four Wheeler, Commercial', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='vehicletype',
            name='wheel',
        ),
    ]
