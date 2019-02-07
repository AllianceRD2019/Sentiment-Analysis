from django import forms
from Document.models import Config

class ConfigForm(forms.ModelForm):
    url = forms.CharField(max_length=250)
    class Meta:
        model = Config
        fields = ('url',)