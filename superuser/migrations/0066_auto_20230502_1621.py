# Generated by Django 3.2.15 on 2023-05-02 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0065_agentscommission'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentscommission',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='agentscommission',
            name='status',
            field=models.CharField(default='Not paid', max_length=100, null=True),
        ),
    ]
