from django.contrib import admin

# Register your models here.
from .models import *
from admin_panel.models import Percent, User, Language, Text, Color

admin.site.register(User)



class TextInline(admin.TabularInline):
    model = Text
    extra = 1



@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    inlines = [ TextInline ]


class PercentInline(admin.TabularInline):
    model = Percent
    extra = 1


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    inlines = [PercentInline]
