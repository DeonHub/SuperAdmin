# Generated by Django 3.2.15 on 2023-02-13 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0039_alter_subscriptions_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountsubscription',
            name='expired',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
