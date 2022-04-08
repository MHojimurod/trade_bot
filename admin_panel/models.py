from multiprocessing import parent_process
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.





class Language(models.Model):
    id: int
    name: str = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
    
    def _(self, name:str, *args, **kwargs) -> str:
        res:Text = Text.objects.filter(name=name, language=self).first()
        return res.data.format(*args, **kwargs) if res is not None else name

class Text(models.Model):
    id: int
    name:str = models.CharField(max_length=100)
    data:str = models.TextField()
    language:Language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
    
    def _(self, name:str, language: Language=None, *args, **kwargs) -> str:
        if language is None:
            res:Text = Text.objects.filter(name=name, language=1).first()
        else:
            res:Text = Text.objects.filter(name=name, language=language).first()
        return res.data.format(*args, **kwargs) if res is not None else name

class Operators(models.Model):
    id: int
    name: str = models.CharField(max_length=200,null=True,blank=True)
    surname : str= models.CharField(max_length=200,null=True,blank=True)
    username: str = models.CharField(max_length=200)
    password: str = models.CharField(max_length=200)
    phone : int= models.IntegerField()
    photo  = models.ImageField(upload_to='images/', default='/static/dashboard/assets/img/default.png')
    region: str= models.CharField(max_length=200,null=True,blank=True)
    address: str= models.CharField(max_length=200,null=True,blank=True)
    token: str= models.CharField(max_length=200)
    active: bool = models.BooleanField(default=False)
    is_have: bool =  models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Fillials(models.Model):
    id: int
    name_uz: str = models.CharField(max_length=200)
    name_ru: str = models.CharField(max_length=200)
    desc_uz: str = RichTextField()
    desc_ru: str = RichTextField()
    active: bool = models.BooleanField(default=False)

    def __str__(self):
        return self.name_ru


class BotSettings(models.Model):
    id: int
    money: int= models.IntegerField(default=0)


class Category(models.Model):
    id: int
    name_uz: str = models.CharField(max_length=200)
    name_ru: str = models.CharField(max_length=200)
    active: bool = models.BooleanField(default=False)
    parent: "Category" = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name_ru


class Product(models.Model):
    id: int
    name_uz: str = models.CharField(max_length=200)
    name_ru: str = models.CharField(max_length=200)
    category: Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo  = models.ImageField(upload_to='images/')
    active: bool = models.BooleanField(default=False)

    def __str__(self):
        return self.name_ru




class Color(models.Model):
    id: int
    color: str = models.CharField(max_length=200)
    base_percent: int = models.PositiveIntegerField()

    def credits(self) -> "Percent":
        return Percent.objects.filter(color=self)
    



class Percent(models.Model):
    id: int
    percent:int = models.PositiveIntegerField()
    color: Color = models.ForeignKey(Color, on_delete=models.CASCADE)


class User(models.Model):
    id: int
    chat_id:int = models.IntegerField()
    language: Language = models.ForeignKey(Language, on_delete=models.SET(1))
    name: str = models.CharField(max_length=200)
    number: str = models.CharField(max_length=200)

    def text(self,name, *args, **kwargs) -> str:
        res: Text = Text.objects.filter(
                name=name, language=self.language).first()
        return res.data.format(*args, **kwargs) if res is not None else name


    def menu(self):
        return [
            [
                self.text
            ]
        ]