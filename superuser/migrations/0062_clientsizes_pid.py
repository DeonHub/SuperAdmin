# Generated by Django 3.2.15 on 2023-05-02 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superuser', '0061_alter_accountsubscription_expires_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientsizes',
            name='pid',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]