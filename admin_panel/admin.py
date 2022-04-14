from django.contrib import admin

# Register your models here.
from admin_panel.models import Operators, Fillials, BotSettings,Product,Color,Category, Busket, BusketItem


admin.site.register(BotSettings)
admin.site.register(Operators)
admin.site.register(Fillials)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Busket)
admin.site.register(BusketItem)



