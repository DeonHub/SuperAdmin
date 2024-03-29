# Generated by Django 3.2.15 on 2022-10-05 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0010_auto_20221005_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialModuleFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_type', models.CharField(max_length=100)),
                ('duration', models.IntegerField(default=0, null=True)),
                ('client', models.CharField(max_length=100)),
                ('module_name', models.CharField(default='None', max_length=20)),
                ('membership_size', models.CharField(default='None', max_length=20)),
                ('unit_fee_usd', models.IntegerField(default=0, null=True)),
                ('unit_fee_ghs', models.IntegerField(default=0, null=True)),
                ('respective_increase', models.IntegerField(default=0, null=True)),
                ('promo', models.BooleanField(default=False, null=True)),
                ('promo_discount', models.IntegerField(default=0, null=True)),
                ('discount_amount_usd', models.IntegerField(default=0, null=True)),
                ('discount_amount_ghs', models.IntegerField(default=0, null=True)),
                ('promo_duration', models.IntegerField(default=0, null=True)),
                ('promo_membership_size', models.CharField(default='None', max_length=20)),
                ('created_by', models.CharField(default='Admin', max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('module', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='superuser.modules')),
            ],
        ),
    ]
