# Generated by Django 3.2.15 on 2022-10-28 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0022_paymentdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivationFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_fee', models.FloatField(default=0.0, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
