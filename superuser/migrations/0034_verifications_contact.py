# Generated by Django 3.2.15 on 2022-12-14 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0033_tuakausers_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='verifications',
            name='contact',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
