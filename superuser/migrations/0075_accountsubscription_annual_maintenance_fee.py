# Generated by Django 3.2.15 on 2023-05-06 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0074_modulefee_client_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountsubscription',
            name='annual_maintenance_fee',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
