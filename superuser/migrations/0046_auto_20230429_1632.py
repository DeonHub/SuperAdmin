# Generated by Django 3.2.15 on 2023-04-29 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0045_agents'),
    ]

    operations = [
        migrations.AddField(
            model_name='agents',
            name='account_name',
            field=models.CharField(default='Demo Account', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='agents',
            name='branch',
            field=models.CharField(default='Main', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='agents',
            name='fullname',
            field=models.CharField(default='None', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='agents',
            name='pid',
            field=models.CharField(default=0, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='agents',
            name='token',
            field=models.CharField(max_length=100, null=True),
        ),
    ]