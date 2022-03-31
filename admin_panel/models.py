from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Operators(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phone = models.IntegerField(max_length=100)
    token = models.CharField(max_length=200)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name