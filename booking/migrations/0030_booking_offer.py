# Generated by Django 3.2 on 2022-02-10 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0029_auto_20220209_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='booking.offer'),
        ),
    ]
