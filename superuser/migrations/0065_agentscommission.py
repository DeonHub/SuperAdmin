# Generated by Django 3.2.15 on 2023-05-02 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0064_auto_20230502_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentsCommission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=100, null=True)),
                ('client_id', models.CharField(max_length=100, null=True)),
                ('agent_name', models.CharField(max_length=100, null=True)),
                ('usercode', models.CharField(max_length=100, null=True)),
                ('commission', models.CharField(max_length=100, null=True)),
                ('amount', models.FloatField(default=0.0, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
