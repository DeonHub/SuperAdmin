from django.db import models

# Create your models here.
class Dasho(models.Model):
    pid = models.IntegerField(null=True, default=0)
    redirected = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pid} was redirected = {self.redirected}'


