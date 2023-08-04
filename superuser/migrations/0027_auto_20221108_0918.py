# Generated by Django 3.2.15 on 2022-11-08 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0026_alter_activationfee_membership_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modulefee',
            name='amount_to_be_paid_ghs',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='modulefee',
            name='amount_to_be_paid_usd',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='modulefee',
            name='discount_amount_ghs',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='modulefee',
            name='discount_amount_usd',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='modulefee',
            name='unit_fee_ghs',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='modulefee',
            name='unit_fee_usd',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
