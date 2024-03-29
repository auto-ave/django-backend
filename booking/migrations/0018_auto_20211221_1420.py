# Generated by Django 3.2 on 2021-12-21 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_user_email'),
        ('store', '0009_auto_20211026_2008'),
        ('booking', '0017_coupon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='discount',
        ),
        migrations.AddField(
            model_name='coupon',
            name='discount_percentage',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='coupon',
            name='linked_store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coupons', to='store.store'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='max_discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='coupon',
            name='max_redeem_count',
            field=models.IntegerField(default=10, help_text='Maximum number of times a coupon can be used in total, 0 for unlimited'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='max_redeem_count_per_cosumer',
            field=models.IntegerField(default=2, help_text='Maximum number of times a coupon can be used by one user, 0 for unlimited'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='priority',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='coupon',
            name='title',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coupon',
            name='valid_from',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='coupon',
            name='valid_to',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='CouponRedeem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='redeems', to='accounts.consumer')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='redeems', to='booking.coupon')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
