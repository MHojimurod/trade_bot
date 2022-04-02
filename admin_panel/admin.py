from django.contrib import admin

# Register your models here.
from admin_panel.models import Operators, Fillials, BotSettings


admin.site.register(BotSettings)
admin.site.register(Operators)
admin.site.register(Fillials)