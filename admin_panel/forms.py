from dataclasses import fields
from django import forms
from admin_panel.models import Ads, Aksiya, Category, Fillials, Operators, Product
import hashlib

class  FillialsForm(forms.ModelForm):
    class Meta:
        model = Fillials
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name_uz','name_ru','active']
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name_uz","name_ru","parent", 'active']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            'color': forms.Select(attrs={
                'class': "form-control",
                
                }),
        }



class OperatorForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    class Meta:
        model = Operators
        fields = ["name","surname","username","password","phone","active","pers","photo"]   

class OperatorEditForm(forms.ModelForm):
    class Meta:
        model = Operators
        fields = ["name","surname","phone","active","pers","photo"]   


class AdsForm(forms.ModelForm):
    class Meta:
        model = Ads
        fields = ["photo","desc"]


class OffersForm(forms.ModelForm):
    class Meta:
        model = Aksiya
        fields = ["name_uz","name_ru","media", 'mode', 'caption']