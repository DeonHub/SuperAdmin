# Generated by Django 3.2.15 on 2023-04-12 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0042_alter_subscriptions_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientSizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=100)),
                ('client_name', models.CharField(max_length=100)),
                ('size', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
