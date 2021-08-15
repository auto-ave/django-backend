# Generated by Django 3.2 on 2021-08-15 18:43

from django.db import migrations, models
import django.db.models.deletion
import django_better_admin_arrayfield.models.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('common', '0001_initial'),
        ('vehicle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified_by_admin', models.BooleanField(default=False, verbose_name='Verified by admin')),
                ('is_locked_for_salesman', models.BooleanField(default=False, verbose_name='Locked for salesmanm if True salesman cannot edit this')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('description', models.TextField(max_length=300)),
                ('thumbnail', models.URLField()),
                ('images', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.URLField(), blank=True, null=True, size=None)),
                ('contact_numbers', django_better_admin_arrayfield.models.fields.ArrayField(base_field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None), size=None)),
                ('address', models.TextField()),
                ('latitude', models.DecimalField(decimal_places=16, max_digits=22)),
                ('longitude', models.DecimalField(decimal_places=16, max_digits=22)),
                ('contact_person_name', models.CharField(max_length=30)),
                ('contact_person_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('contact_person_photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('store_times', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.JSONField(), help_text='{"closing_time": "18:00:00", "opening_time": "09:00:00"}', size=None)),
                ('slot_length', models.PositiveIntegerField()),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='common.city')),
                ('owner', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.storeowner')),
                ('partner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stores', to='accounts.partner')),
                ('salesman', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stores', to='accounts.salesman')),
                ('supported_vehicle_types', models.ManyToManyField(blank=True, related_name='stores', to='vehicle.VehicleType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_blocking', models.BooleanField()),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('bay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='store.bay')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bay',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bays', to='store.store'),
        ),
        migrations.AddField(
            model_name='bay',
            name='supported_vehicle_types',
            field=models.ManyToManyField(blank=True, to='vehicle.VehicleType'),
        ),
        migrations.CreateModel(
            name='PriceTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('price', models.PositiveIntegerField()),
                ('time_interval', models.PositiveIntegerField()),
                ('images', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.URLField(), blank=True, null=True, size=None)),
                ('description', models.TextField()),
                ('bays', models.ManyToManyField(blank=True, help_text='BUG: Do no edit this field, if you want to change bays delete this instance and create another one', to='store.Bay')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pricetimes', to='common.service')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pricetimes', to='store.store')),
                ('vehicle_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pricetimes', to='vehicle.vehicletype')),
            ],
            options={
                'unique_together': {('vehicle_type', 'service')},
            },
        ),
    ]
