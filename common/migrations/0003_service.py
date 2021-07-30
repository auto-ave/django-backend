# Generated by Django 3.2 on 2021-07-20 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_alter_city_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
