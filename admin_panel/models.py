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

    def category_list(self, page:int=1, parent:int = None):
        keyboard = []
        categorys = list(Category.objects.filter(parent=parent, active=True) if parent is not None else Category.objects.filter(parent=None, active=True))
        categorys_count = len(categorys)
        categorys_per_page = 10
        categorys_pages = categorys_count // categorys_per_page + \
            1 if categorys_count % categorys_per_page != 0 else categorys_count // categorys_per_page
        
        categorys_page = categorys[(
            page - 1) * categorys_per_page:page * categorys_per_page]
        
        categorys_page_inline = [  ]
        text = "Katalog\n\n"
        for i in range(len(categorys_page)):
            category = categorys_page[i]
            text += f"{i + 1}. {category.name(self.language)}\n"
            categorys_page_inline.append(
                InlineKeyboardButton(
                    str(i + 1), callback_data=f"select_category:{category.id}")
            )
        keyboard = distribute(categorys_page_inline, 5)

        controls = []
        if page > 1:
            controls.append(InlineKeyboardButton(
                "⬅️", callback_data=f"category_pagination:{page - 1}"))
        controls.append(InlineKeyboardButton(
            "🔙", callback_data=f"cancel_pagination"),)

        if page < categorys_pages:
            controls.append(InlineKeyboardButton(
                "➡️", callback_data=f"category_pagination:{page + 1}"))
        keyboard.append(controls)

        return {
            "text": text,
            "reply_markup": InlineKeyboardMarkup(keyboard)
        }

    
    def product_list(self, page:int=1, category:Category=None):
        keyboard = []
        products = list(Product.objects.filter(category=category, active=True))
        products_count = len(products)
        products_per_page = 10
        products_pages = products_count // products_per_page + \
            1 if products_count % products_per_page != 0 else products_count // products_per_page

        products_page = products[(
            page - 1) * products_per_page:page * products_per_page]

        products_page_inline = []
        text = "Katalog\n\n"
        for i in range(len(products_page)):
            product: Product = products_page[i]
            text += f"{i + 1}. {product.name(self.language)}\n"
            products_page_inline.append(
                InlineKeyboardButton(
                    str(i + 1), callback_data=f"select_product:{product.id}")
            )
        keyboard = distribute(products_page_inline, 5)

        controls = []
        if page > 1:
            controls.append(InlineKeyboardButton(
                "⬅️", callback_data=f"category_pagination:{page - 1}"))
        controls.append(InlineKeyboardButton(
            "🔙", callback_data=f"cancel_pagination"),)

        if page < products_pages:
            controls.append(InlineKeyboardButton(
                "➡️", callback_data=f"category_pagination:{page + 1}"))
        keyboard.append(controls)

        return {
            "text": text,
            "reply_markup": InlineKeyboardMarkup(keyboard)
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