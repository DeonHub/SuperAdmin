# Generated by Django 3.2.15 on 2023-05-04 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0071_auto_20230504_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='agents',
            name='gender',
            field=models.IntegerField(default=1, null=True),
        ),
    ]
