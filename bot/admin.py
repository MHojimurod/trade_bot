from django.contrib import admin

# Register your models here.
from .models import *
from admin_panel.models import User, Language, Text

admin.site.register(User)



class TextInline(admin.TabularInline):
    model = Text
    extra = 1



@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    inlines = [ TextInline ]