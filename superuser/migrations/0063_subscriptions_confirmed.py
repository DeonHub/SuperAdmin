# Generated by Django 3.2.15 on 2023-05-02 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0062_clientsizes_pid'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptions',
            name='confirmed',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
