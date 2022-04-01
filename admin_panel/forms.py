from django import forms
from admin_panel.models import Fillials


class FillialsForm(forms.ModelForm):
    class Meta:
        model = Fillials
        fields = "__all__"