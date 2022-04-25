from typing import Text
from django.contrib import admin

# Register your models here.
from admin_panel.models import Aksiya, Operators, Fillials, BotSettings,Product,Color,Category, Busket, BusketItem,Percent, Text,Ads


admin.site.register(BotSettings)
admin.site.register(Operators)
admin.site.register(Fillials)
admin.site.register(Product)
admin.site.register(Busket)
admin.site.register(BusketItem)
admin.site.register(Percent)
admin.site.register(Text)





class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryInline, ProductInline]

admin.site.register(Aksiya)
admin.site.register(Ads)

