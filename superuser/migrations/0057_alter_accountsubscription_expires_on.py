# Generated by Django 3.2.15 on 2023-04-30 17:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0056_alter_accountsubscription_expires_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountsubscription',
            name='expires_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
