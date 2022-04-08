from django import forms
from admin_panel.models import Category, Fillials, Operators, Product
import hashlib

class  FillialsForm(forms.ModelForm):
    class Meta:
        model = Fillials
        fields = "__all__"


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['active']
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["parent", 'active']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

class OperatorForm(forms.ModelForm):
    class Meta:
        model = Operators
        fields = ["name","surname","username","password","phone","active"]