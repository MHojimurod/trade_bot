from django.contrib import admin

# Register your models here.
from admin_panel.models import Operators, Fillials, BotSettings,Product,Color,Category


admin.site.register(BotSettings)
admin.site.register(Operators)
admin.site.register(Fillials)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Product)