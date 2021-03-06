from datetime import datetime
import locale
from re import T
from django.db import models
from ckeditor.fields import RichTextField
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, Update
from telegram.ext import CallbackContext
from django.db.models.query import QuerySet
from django.contrib.auth.models import User as DjangoUser
from multiselectfield import MultiSelectField
from django.core.validators import FileExtensionValidator
val=[FileExtensionValidator(allowed_extensions=['mp4', 'jpg','png','mow','avi','3gp',"gif"])]
# from tg_bot.utils import distribute


def distribute(items, number):
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


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def money(number: int, grouping: bool = True):
    return f"{locale.currency(number, grouping=grouping).split('.')[0][1:]}"


class Name:
    def name(self, language: "Language" = None) -> str:
        if language is None:
            return self.name_uz
        return self.__getattribute__(f"name_{language.code}")


class Language(models.Model):
    id: int
    name: str = models.CharField(max_length=100)
    code = models.CharField(max_length=3, unique=True)

    def money(self):
        return {
            "uz": "so'm",
            "ru": "сум",
            "en": "sums"
        }[self.code]

    def month(self):
        return {
            "uz": "oy",
            "ru": "месяц",
            "en": "month"
        }[self.code]

    def __str__(self) -> str:
        return self.name + " (" + str(self.id) + ")"

    def _(self, name: str, *args, **kwargs) -> str:
        res: Text = Text.objects.filter(name=name, language=self).first()
        return res.data.format(*args, **kwargs) if res is not None else name
    
    def texts(self) -> QuerySet:
        return Text.objects.filter(language=self)
    
    def save(self):
        super().save()
        self.sync()
    
    def sync(self):
        print("xxx")
        text_names = []
        text: Text

        for text in Text.objects.all():
            if text.name not in text_names:
                text_names.append({
                    "name": text.name,
                    "data": text.data,
                })
                # print(text.name, self)

        for text_name in text_names:
            if Text.objects.filter(name=text_name["name"], language=self).first() is None:
                Text.objects.create(
                    name=text_name["name"],
                    data=text_name["data"],
                    language=self
                )
        
            


class Text(models.Model):
    id: int
    name: str = models.CharField(max_length=100)
    data: str = models.TextField()
    language: Language = models.ForeignKey(Language, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.name

    def _(self, name: str, language: Language = None, *args, **kwargs) -> str:
        if language is None:
            res: Text = Text.objects.filter(name=name, language=1).first()
        else:
            res: Text = Text.objects.filter(
                name=name, language=language).first()
        return res.data.format(*args, **kwargs) if res is not None else name
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        Text.objects.filter(name=self.name).delete()
    
    def save(self, *args, **kwargs):
        # super().save(*args, **kwargs)
        if self.pk is not None:
            initial = Text.objects.get(pk=self.pk)
            if initial:
                if self.name != initial.name:
                    Text.objects.filter(name=initial.name).delete()
        super().save(*args, **kwargs)

        for lang in Language.objects.all():
            lang.sync()
            

    

class Operators(models.Model):
    access  =(
        ("statistic","Statistika"),
        ("operators","Operatorlar"),
        ("category","Kategoriya"),
        ("ads","Reklama"),
        ("fillial","Filliallar"),
        ("present","Aksiyalar"),
        ("settings","Bot Sozlamalari"),
        ("text","Textlar"),
        ("followers","Foydalanuvchilar"),
        ("comments","Kommentariyalar"),
    )
    
    id: int
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username=  models.CharField(max_length=100)
    password2 = models.CharField(max_length=999999)

    phone: int = models.IntegerField()
    photo = models.ImageField(
        upload_to='images/', default='/static/dashboard/assets/img/default.png', null=True, blank=True)
    region: str = models.CharField(max_length=200, null=True, blank=True)
    address: str = models.CharField(max_length=200, null=True, blank=True)
    active: bool = models.BooleanField(default=False)
    is_have: bool = models.BooleanField(default=False)
    pers = MultiSelectField(choices=access)

    def __str__(self):
        return self.user.first_name


class Fillials(models.Model):
    id: int
    name_uz: str = models.CharField(max_length=200)
    name_ru: str = models.CharField(max_length=200)
    desc_uz: str = RichTextField()
    desc_ru: str = RichTextField()



    def desc_uz_get(self):
        return self.desc_uz.replace("<p>", "").replace("</p>", "").replace("<strong>", "<b>").replace("</strong>", "</b>").replace("<em>", "<i>").replace("</em>", "</i>").replace("<br />","\n").replace("\r\n\r\n", "\n").replace("&nbsp;", " ")

    def desc_ru_get(self):
        return self.desc_ru.replace("<p>", "").replace("</p>", "").replace("<strong>", "<b>").replace("</strong>", "</b>").replace("<em>", "<i>").replace("</em>", "</i>").replace("<br />","\n").replace("\r\n\r\n", "\n").replace("&nbsp;", " ")

    
    
    def desc_uz_set(self, new):
        self.desc_uz = new
        self.save()

    def desc_ru_set(self, new):
        self.desc_ru = new
        self.save()
    
    _desc_uz = property(desc_uz_get, desc_uz_set)
    _desc_ru = property(desc_ru_get, desc_ru_set)



    active: bool = models.BooleanField(default=False)

    def __str__(self):
        return self.name_ru

    def name(self, language: Language = None) -> str:
        if language is None:
            return self.name_uz
        return self.__getattribute__(f"name_{language.code}")

    def desc(self, language: Language = None) -> str:
        if language is None:
            return self.name_uz
        return self.__getattribute__(f"desc_{language.code}_get")()
    
    def address(self, language: Language = None) -> str:
        return f"{self.name(language)}\n\n{self.desc(language)}"

    


class BotSettings(models.Model):
    id: int
    money: int = models.IntegerField(default=0)
    request_self_image = models.ImageField(null=True, blank=True)
    request_passport_image = models.ImageField(null=True, blank=True)
    request_self_passport_image = models.ImageField(null=True, blank=True)


class Category(models.Model):
    id: int
    name_uz: str = models.CharField(max_length=200)
    name_ru: str = models.CharField(max_length=200)

    active: bool = models.BooleanField(default=False)
    parent: "Category" = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f" {self.name_uz} | cats {len(self.sub_categories())} - products {len(self.products())} { f'sub {self.parent.name_uz}' if self.parent else ''} "

    def name(self, language: Language = None) -> str:
        if language is None:
            return self.name_uz
        return self.__getattribute__(f"name_{language.code}")

    def products(self) -> "list[Product]":
        # return Product.objects.filter(category=self).exclude(desc_uz="", desc_ru="")
        return Product.objects.filter(category=self)

    def sub_categories(self) -> "list[Category]":
        return Category.objects.filter(parent=self)
    
    @property
    def sold_products(self):
        return sum(i.sold_products_sub() for i in self.sub_categories())
    
    def sold_products_sub(self):
        return sum( i.monthly_sold() for i in self.products())



class Product(models.Model):
    id: int
    name_uz: str = models.CharField(max_length=200)
    name_ru: str = models.CharField(max_length=200)
    category: Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/')
    active: bool = models.BooleanField(default=False)
    tan_price: int = models.IntegerField()
    color: "Color" = models.ForeignKey("Color", on_delete=models.CASCADE, null=True, blank=True)
    desc_uz: str = RichTextField(default="", blank=True)
    desc_ru: str = RichTextField(default="", blank=True)

    def monthly_sold(self):
        return sum(
            [i.count for i in [j for j in BusketItem.objects.filter(product=self) if j.busket.is_ordered]]
        )



    def desc_uz_get(self):
        print(self.desc_uz.encode())
        return self.desc_uz.replace("<p>", "").replace("</p>", "").replace("<strong>", "<b>").replace("</strong>", "</b>").replace("<em>", "<i>").replace("</em>", "</i>").replace("\r\n\r\n", "\n").replace("&nbsp;", " ").replace("<br />","\n")

    def desc_ru_get(self):
        print(self.desc_ru)
        return self.desc_ru.replace("<p>", "").replace("</p>", "").replace("<strong>", "<b>").replace("</strong>", "</b>").replace("<em>", "<i>").replace("</em>", "</i>").replace("\r\n\r\n", "\n").replace("&nbsp;", " ").replace("<br />","\n")

    
    
    def desc_uz_set(self, new):
        self.desc_uz = new
        self.save()

    def desc_ru_set(self, new):
        self.desc_ru = new
        self.save()
    
    _desc_uz = property(desc_uz_get, desc_uz_set)
    _desc_ru = property(desc_ru_get, desc_ru_set)

    def desc(self, language: Language = None) -> str:
            if language is None:
                return self.name_uz
            return self.__getattribute__(f"desc_{language.code}_get")()
    
    def has_description(self):
        return self.desc_uz != "" and self.desc_ru != ""


    @property
    def p(self):
        return self.tan_price * BotSettings.objects.first().money

    def price(self, month: "Percent"):
        return (self.p + (((self.p // 100) * month.percent)))
    
    def percents(self):
        pass

    def name(self, language: Language = None) -> str:
        if language is None:
            return self.name_uz
        return self.__getattribute__(f"name_{language.code}")

    def __str__(self):
        return self.name_ru





class Color(models.Model):
    id: int
    color: str = models.CharField(max_length=200)
    base_percent: int = models.PositiveIntegerField()

    @property
    def months(self):
        return Percent.objects.filter(color=self).exclude(percent=0)
    def __str__(self) -> str:
        return self.color


class Percent(models.Model):
    id: int
    color: Color = models.ForeignKey(Color, on_delete=models.CASCADE)
    months: int = models.IntegerField()
    percent: int = models.IntegerField()



class User(models.Model):
    id: int
    chat_id: int = models.IntegerField()
    language: Language = models.ForeignKey(Language, on_delete=models.SET(1))
    name: str = models.CharField(max_length=200)
    number: str = models.CharField(max_length=200)
    filial: Fillials = models.ForeignKey(Fillials, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def settings(self):
        return [
            [
                self.text('change_name'),
                self.text('change_number'),
            ],
            [
                self.text('change_language'),
                self.text('change_filial')
            ],
            [
                self.text('back')
            ]
        ]
    
    def get_orders(self):
        bs: list[Busket] = Busket.objects.filter(user=self, bis_ordered=True)
        res = []
        for b in bs:
            if b.products.count() > 0:
                res.append(b)
        return res

    def text(self, namee, *args, **kwargs) -> str:
        res: Text = Text.objects.filter(name=namee, language=self.language).first()
        return res.data.format(*args, **kwargs) if res is not None else namee


    def category_list(self, page: int = 1, parent: int = None, context: CallbackContext = None, user:"User"=None):
        keyboard = []
        categorys = list(Category.objects.filter(parent=parent, active=True)
                         if parent is not None else Category.objects.filter(parent=None, active=True))
        categorys_count = len(categorys)
        categorys_per_page = 9
        categorys_pages = categorys_count // categorys_per_page + \
            1 if categorys_count % categorys_per_page != 0 else categorys_count // categorys_per_page

        categorys_page = categorys[(
            page - 1) * categorys_per_page:page * categorys_per_page]

        categorys_page_inline = []
        text = f"{self.text('categorys')}\n\n"
        for i in range(len(categorys_page)):
            category = categorys_page[i]
            # text += f"{i + 1}. {category.name(self.language)}\n"
            categorys_page_inline.append(
                InlineKeyboardButton(
                    category.name(self.language), callback_data=f"select_category:{category.id}")
            )
        keyboard = distribute(categorys_page_inline, 3)

        if user.busket.is_available and parent == None:
            keyboard.append([
                InlineKeyboardButton(self.text('busket_button'), callback_data="cart")
            ])

        controls = []
        controls.append(InlineKeyboardButton(
            user.text('back'), callback_data=f"back_to_category_from_category"),)
        if page > 1:
            controls.append(InlineKeyboardButton(
                "⬅️", callback_data=f"category_pagination:{page - 1}"))

        if page < categorys_pages:
            controls.append(InlineKeyboardButton(
                "➡️", callback_data=f"category_pagination:{page + 1}"))
        keyboard.append(controls)

        return {
            "text": text,
            "reply_markup": InlineKeyboardMarkup(keyboard)
        }
    

    def product_list(self, page: int = 1, category: Category = None):
        keyboard = []
        products = list(Product.objects.filter(category=category, active=True))
        products_count = len(products)
        products_per_page = 10
        products_pages = products_count // products_per_page + \
            1 if products_count % products_per_page != 0 else products_count // products_per_page

        products_page = products[(
            page - 1) * products_per_page:page * products_per_page]

        products_page_inline = []
        text = f"{self.text('categorys')}\n\n"
        for i in range(len(products_page)):
            product: Product = products_page[i]
            text += f"{i + 1}. {product.name(self.language)}\n"
            products_page_inline.append(
                InlineKeyboardButton(
                    str(i + 1), callback_data=f"select_product:{product.id}")
            )
        keyboard = distribute(products_page_inline, 5)

        controls = []
        controls.append(InlineKeyboardButton(
            self.text('back'), callback_data=f"back_to_category_from_category"),)
        if page > 1:
            controls.append(InlineKeyboardButton(
                self.text('⬅️'), callback_data=f"category_pagination:{page - 1}"))

        if page < products_pages:
            controls.append(InlineKeyboardButton(
                "➡️", callback_data=f"category_pagination:{page + 1}"))
        keyboard.append(controls)

        return {
            "text": text,
            "reply_markup": InlineKeyboardMarkup(keyboard)
        }

    def product_info(self, context: CallbackContext, photo:bool=True, user: "User"=None):


        keyboard = []
        count_controls = []
        product: Product = context.user_data['order']['current_product']['product']
        product.refresh_from_db()
        text = f"<b>{product.name(user.language)}</b>\n"
        if product.has_description():
            text += "\n" + product.desc(user.language) + "\n\n"
        per_month = 0

        if not context.user_data['order']['current_product']['month']:
            for i in product.color.months:
                text += """    <b>{per_month} x {months} {month_text} x {count} ta = {price} {money}</b>\n""".format(
                per_month=money(product.price(i) // i.months),
                months=i.months,
                price=money(product.price(i)),
                pr_name=product.name(user.language),
                count=context.user_data['order']['current_product']['count'],
                month_text=user.language.month(),
                money=user.language.money(),
    )

        else:
            month: Percent = context.user_data['order']['current_product']['month']


            text += """    <b>{per_month} x {months} {month_text} x {count} ta = {price} {money}</b>\n""".format(
                per_month=money(product.price(month) // month.months),
                months=month.months,
                price=money(product.price(month)),
                pr_name=product.name(user.language),
                count=context.user_data['order']['current_product']['count'],
                month_text=user.language.month(),
                money=user.language.money(),
            )
            per_month += (product.price(month) // month.months) * context.user_data['order']['current_product']['count']
        

        if context.user_data['order']['current_product']['count'] > 1:
            count_controls.append(
                InlineKeyboardButton("-", callback_data=f"product_count:-"))

        count_controls.append(
            InlineKeyboardButton(
                str(context.user_data['order']['current_product']['count']), callback_data=f"just"))

        count_controls.append(
            InlineKeyboardButton("+", callback_data=f"product_count:+"))

        keyboard.append(count_controls)

        # keyboard.append([
        #     InlineKeyboardButton(str(i + 1), callback_data=f"product_count:{i + 1}") for i in range(3)
        # ])
        # keyboard.append([
        #     InlineKeyboardButton(str(i + 1), callback_data=f"product_count:{i + 1}") for i in range(3, 6)
        # ])
        # keyboard.append([
        #     InlineKeyboardButton(str(i + 1), callback_data=f"product_count:{i + 1}") for i in range(6, 9)
        # ])
        x = {
            "uz": f"Bir oylik to'lov: {money(per_month)} so'm",
            "ru": f"Ежемесячный платеж: {money(per_month)} сум.",
            "en": f"Monthly payment: {money(per_month)} so'm"
        }[self.language.code]

        text += f'<b>{x}</b>'

        keyboard.append([
            InlineKeyboardButton(
                f"{i.months} {self.language.month()} {'✅' if context.user_data['order']['current_product']['month'] == i else ''}", callback_data=f"product_creadit_month:{i.id}") for i in product.color.months.exclude(months=0)
        ])
        



        keyboard.append(
            [
                InlineKeyboardButton(
                   user.text('back'), callback_data=f"back_to_category_from_product"),
                InlineKeyboardButton(
                    user.text("clearance"), callback_data=f"add_to_cart"),
            ]
        )
        if photo:
            return {
                "photo": open(f".{context.user_data['order']['current_product']['product'].photo.url}", 'rb'),
                "caption": text,
                "reply_markup": InlineKeyboardMarkup(keyboard)
            }
        else:
            return {
                "caption": text,
                "reply_markup": InlineKeyboardMarkup(keyboard)
            }

    def cart(self, context: CallbackContext, user:"User", back_to_category:bool=True):
        text = ""
        obshiy_summa = 0
        pr_texts = []
        keyboard = []
        busket = user.busket
        x = {"uz": "Oyiga",
            "ru": "За месяц",
            "en": "per month"}[self.language.code]
        if busket.is_available:
            for pr in busket.products:
                obshiy_summa += pr.product.price(pr.month) * pr.count
                pr_texts.append(f"""{pr.product.name(user.language)}
        {money(pr.product.price(pr.month) // pr.month.months)} {self.language.money()} x {pr.month.months} {self.language.month()} = {money(pr.product.price(pr.month))}  {self.language.money()}
        {money(pr.product.price(pr.month))} {self.language.money()} x {pr.count} = {money(pr.product.price(pr.month) * pr.count)} {self.language.money()}
        { x }: {money((pr.product.price(pr.month) // pr.month.months)  * pr.count) } {self.language.money()}""")
                controls = []
                if pr.count > 1:
                    controls.append(
                        InlineKeyboardButton(
                            "-", callback_data=f"cart_item_count:-:{pr.id}"
                        )
                    )
                controls.append(InlineKeyboardButton(str(pr.count), callback_data="just"))
                controls.append(InlineKeyboardButton(
                    "❌", callback_data=f"remove_from_cart:{pr.id}"))
                controls.append(
                    InlineKeyboardButton(
                        "+", callback_data=f"cart_item_count:+:{pr.id}"
                    )
                )
                keyboard.append(controls)
            keyboard.append([InlineKeyboardButton(
                "➕" + user.text("add_more"), callback_data=f"cart_add_more")])
        
            
            keyboard.append([
                InlineKeyboardButton(
                    self.text('back'), callback_data=f"back_to_category_from_cart" if back_to_category else "back_to_menu_from_cart"),
                        InlineKeyboardButton(self.text("clearance"), callback_data=f"order_cart"),

            ])
            y = {
                "uz": "Umumiy summa",
                "ru": "Общая сумма",
                "en": "Total amount"
            }[self.language.code]
            text += "\n———————————————-\n".join(pr_texts)
            text += f"\n\n{y}: {money(obshiy_summa)}  {self.language.money()}"
        else:
            text = self.text("cart_empty")
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
    
    @property
    def busket(self) -> "Busket":
        res = Busket.objects.filter(user=self, bis_ordered=False).first()
        return res if res else Busket.objects.create(user=self)

class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Busket(models.Model):
    id: int
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    bis_ordered: bool = models.BooleanField(default=False)
    order_time = models.DateTimeField(null=True, blank=True)
    work_place = models.CharField(max_length=100, null=True, blank=True)
    live_place = models.CharField(max_length=100, null=True, blank=True)

    def get_is_ordered(self):
        return self.bis_ordered and self.products.count() > 0
    def set_is_ordered(self, value):
        self.bis_ordered = value
        self.save()

    is_ordered = property(get_is_ordered, set_is_ordered)

    self_image = models.ImageField(upload_to="media/busket", null=True, blank=True)
    passport_image = models.ImageField(upload_to="media/busket", null=True, blank=True)
    self_password_image = models.ImageField(upload_to="media/busket", null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET(
        None), null=True, blank=True)
    extra_number = models.CharField(max_length=20, null=True, blank=True)
    comment = models.TextField(null=True,blank=True)
    status = models.IntegerField(choices=(
        (0, "Kutilmoqda"),
        (1, "Qabul qilindi"),
        (2, "Rad etildi"),
        (3, "Tasdiqlandi!"),
        (4, "Tasdiqlanmadi"),
        (5, "Arxiv"),

    ), default=0)
    actioner = models.ForeignKey(
        Operators, on_delete=models.SET_NULL, null=True, blank=True, related_name="actioner")

    @property
    def is_available(self):
        return bool(self.products.count())

    @property
    def products(self):
        return BusketItem.objects.filter(busket=self)
    
    def add(self, product: Product, count:int,month:Percent):
        x:BusketItem = self.products.filter(product=product).first()
        if not x:
            return BusketItem.objects.create(busket=self, product=product, _count=count, month=month)
        else:
            x.count = count
            return x
    
    def set_location(self, latitude:float, longitude:float):
        self.location = Location.objects.create(user=self.user, latitude=latitude, longitude=longitude)
        self.save()
    
    def set_self_image(self, image):
        self.self_image = image
        self.save()
    
    def set_passport_image(self, image):
        self.passport_image = image
        self.save()

    def set_self_passport_image(self, image):
        self.self_password_image = image
        self.save()
    
    def set_work_place(self, work_place):
        self.work_place = work_place
        self.save()
    
    def set_live_place(self, live_place):
        self.live_place = live_place
        self.save()
    
    def set_extra_number(self, number):
        self.extra_number = number
        self.save()
    
    def order(self):
        self.is_ordered = True
        self.order_time = datetime.now()
        self.save()



class BusketItem(models.Model):
    busket: Busket = models.ForeignKey(Busket, on_delete=models.CASCADE)
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    month: Percent = models.ForeignKey(Percent, on_delete=models.CASCADE)
    _count: int = models.IntegerField()


    def set_count(self, other):
        self._count = other
        self.save()
        
    def get_count(self): return self._count

    count = property(get_count, set_count)









class Aksiya(models.Model, Name):
    name_uz = models.CharField(max_length=15)
    name_ru = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    mode = models.IntegerField(default=0,choices=[
        (0, 'text'),
        (1, "image"),
        (2, 'video')

    ])
    media = models.FileField(null=True, blank=True)
    caption = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name_uz

    @classmethod
    def keyboard(self, language: Language):
        res = []
        i: Aksiya
        for i in self.objects.all():
            res.append(i.name(language))
        return res
    @property
    def file(self):
        return open(f"{self.media.path}", 'rb')


class Support(models.Model):
    data = models.TextField(blank=True)
    media = models.FileField(null=True, blank=True)
    media_type = models.IntegerField(default=0,choices=[
        (0, 'text'),
        (1, "image"),
        (2, 'video')
    ])
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    


class Ads(models.Model):
    mode = models.IntegerField(default=0, choices=[
        (0, 'text'),
        (1, "image"),
        (2, 'video')
        
    ])
    photo = models.FileField(upload_to="images/",null=True, blank=True,validators=val)
    desc = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def send_desc(self):
        return self.desc.replace("<p>", "").replace("</p>", "").replace("<strong>", "<b>").replace("</strong>", "</b>").replace("<em>", "<i>").replace("</em>", "</i>").replace("<br />","\n").replace("\r\n\r\n", "\n").replace("&nbsp;", " ")


[].reverse

# get 