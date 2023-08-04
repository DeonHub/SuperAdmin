# Generated by Django 3.2.15 on 2022-10-01 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0002_membershipsizes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modulefee',
            old_name='subscription_duration',
            new_name='duration',
        ),
        migrations.RemoveField(
            model_name='modulefee',
            name='account_category',
        ),
        migrations.RemoveField(
            model_name='modulefee',
            name='description',
        ),
        migrations.AlterField(
            model_name='modulefee',
            name='membership_size',
            field=models.CharField(default='None', max_length=20),
        ),
    ]
