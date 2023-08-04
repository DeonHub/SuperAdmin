# from jsonfield import JSONField
from django.utils import timezone
from django.db import models


# Create your models here.
class SubFee(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)
    amount = models.FloatField(null=True, default=0.00)
    order_id = models.CharField(null=True, default="ASL20220010", max_length=100)
    confirmed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}'


class DatabaseDetails(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    client = models.CharField(null=True, default="Lord", max_length=100)
    subscribed = models.BooleanField(default=False)
    expires_on = models.DateTimeField( default=timezone.now )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}'



class OneTimeDetails(models.Model):
    client_id = models.CharField(null=True, default="1", max_length=100)
    paid = models.BooleanField(default=False)
    expires_on = models.DateTimeField( default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client_id}'