# Generated by Django 3.2.15 on 2023-04-30 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0053_clientsizes_client_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentclients',
            name='account_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
