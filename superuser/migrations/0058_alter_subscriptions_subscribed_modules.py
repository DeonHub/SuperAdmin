# Generated by Django 3.2.15 on 2023-04-30 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0057_alter_accountsubscription_expires_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions',
            name='subscribed_modules',
            field=models.JSONField(null=True),
        ),
    ]
