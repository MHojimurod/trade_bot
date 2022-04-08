import html
from multiprocessing import parent_process
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.
class Operators(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    surname = models.CharField(max_length=200,null=True,blank=True)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    phone = models.IntegerField()
    photo  = models.ImageField(upload_to='images/', default='/static/dashboard/assets/img/default.png')
    region = models.CharField(max_length=200,null=True,blank=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    token = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    is_have =  models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Fillials(models.Model):
    name_uz = models.CharField(max_length=200)
    name_ru = models.CharField(max_length=200)
    desc_uz = RichTextField()
    desc_ru = RichTextField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name_ru


class BotSettings(models.Model):
    money = models.IntegerField(default=0)


class Category(models.Model):
    name_uz = models.CharField(max_length=200)
    name_ru = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name_ru


class Product(models.Model):
    name_uz = models.CharField(max_length=200)
    name_ru = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo  = models.ImageField(upload_to='images/')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name_ru




class Color(models.Model):
    color = models.CharField(max_length=200)
    base_percent = models.PositiveIntegerField()

    def credits(self):
        return Percent.objects.filter(color=self)
    



class Percent(models.Model):
    percent = models.PositiveIntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE)