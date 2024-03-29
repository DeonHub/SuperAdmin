# Generated by Django 3.2.15 on 2023-04-30 02:13

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0050_modulefee_agent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modulefee',
            name='agent',
        ),
        migrations.RemoveField(
            model_name='modulefee',
            name='agent_unit_fee_ghs',
        ),
        migrations.RemoveField(
            model_name='modulefee',
            name='agent_unit_fee_usd',
        ),
        migrations.RemoveField(
            model_name='modulefee',
            name='usercode',
        ),
        migrations.AddField(
            model_name='modulefee',
            name='agent_cost',
            field=jsonfield.fields.JSONField(default='', null=True),
        ),
    ]
