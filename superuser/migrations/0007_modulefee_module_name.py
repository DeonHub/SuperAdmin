# Generated by Django 3.2.15 on 2022-10-04 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0006_modulefee'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulefee',
            name='module_name',
            field=models.CharField(default='None', max_length=20),
        ),
    ]
