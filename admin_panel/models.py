from multiprocessing import parent_process
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton

# from tg_bot.utils import distribute


def distribute(items, number) -> list:
    res = []
    start = 0
    end = number
    for item in items:
        if items[start:end] == []:
            return res
        res.append(items[start:end])
        start += number
        end += number
    return res
# Create your models here.





class Language(models.Model):
    id: int
    name: str = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)

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
    parent: "Category" = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name_ru
    
    def name(self, language: Language=None) -> str:
        if language is None:
            return self.name_uz
        return self.__getattribute__(f"name_{language.code}")

    def products(self):
        return Product.objects.filter(category=self)

    def sub_categories(self):
        return Category.objects.filter(parent=self)

class Product(models.Model):
    id: int
    name_uz: str = models.CharField(max_length=200)
    name_ru: str = models.CharField(max_length=200)
    category: Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo  = models.ImageField(upload_to='images/')
    active: bool = models.BooleanField(default=False)

    def name(self, language: Language=None) -> str:
        if language is None:
            return self.name_uz
        return self.__getattribute__(f"name_{language.code}")

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

    def category_list(self, page:int=0, per:int=10, id:str = None):
        

        keyboard = []
        if id is None:
            categories: list[Category] = Category.objects.filter(
                parent=None)
        else:
            category: Category = Category.objects.get(pk=id)
            categories: list[Category] = category.sub_categories()
            products : list[Product] = category.products()
        
        
        categories = categories[page * per: (page + 1) * per]

        text = "Categories {page_start}-{page_end} of {total}.\n\n".format(page_start=page * per, page_end=(page * per) +
                                                                              len(categories[page * per: (page + 1) * per]), total=len(categories))
        categories = categories[page * per: (page + 1) * per]
        for i in range(len(categories)):
            text += f"{i + 1}. {categories[i].name(self.language)}\n"
            keyboard.append(InlineKeyboardButton(
               str(i + 1),
               callback_data=f"enter_category_{categories[i].id}"))
        
        
        return {
            "text": text,
            "reply_markup": InlineKeyboardMarkup([ *distribute(keyboard, 5), 
                [InlineKeyboardButton("<", callback_data=f"category_list:{page - 1}"),
                InlineKeyboardButton(">", callback_data=f"category_list:{page + 1}")]
            ])
        }


        
        


    def menu(self):
        return [
            [
                self.text('order'),
                self.text('my_orders'),

            ],
            [
                self.text('busket'),
                self.text('offers'),
            ],
            [
                self.text('our_addresses'),
                self.text('communications'),
            ],
            [
                self.text('settings'),
                self.text('questions_and_adds'),
            ]
        ]