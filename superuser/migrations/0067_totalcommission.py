# Generated by Django 3.2.15 on 2023-05-02 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0066_auto_20230502_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalCommission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usercode', models.CharField(max_length=100, null=True)),
                ('amount', models.FloatField(default=0.0, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('status', models.CharField(default='Not paid', max_length=100, null=True)),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
