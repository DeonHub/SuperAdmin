# Generated by Django 3.2.15 on 2022-10-04 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0007_modulefee_module_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='membershipsizes',
            name='unit_cost_ghs',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='membershipsizes',
            name='unit_cost_usd',
            field=models.IntegerField(default=0, null=True),
        ),
    ]