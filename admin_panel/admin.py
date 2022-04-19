from django.contrib import admin

# Register your models here.
from admin_panel.models import Operators, Fillials, BotSettings,Product,Color,Category, Busket, BusketItem,Percent


admin.site.register(BotSettings)
admin.site.register(Operators)
admin.site.register(Fillials)
admin.site.register(Product)
admin.site.register(Busket)
admin.site.register(BusketItem)
admin.site.register(Percent)




class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]
