from django import forms
from Document.models import Config, InputFile

class ConfigForm(forms.ModelForm):
    url = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder':'https://www.example.com'}), label='')
    class Meta:
        model = Config
        fields = ('url',)
        widgets = {
            'url': forms.ClearableFileInput(attrs={'type':'text', 
                                                    'id':'url',
                                                    'name':'url', 
                                                    }),
        }
        
    
class CsvUploadForm(forms.ModelForm):
    class Meta:
        model = InputFile
        fields = ('csvFile',)
        widgets = {
            # 'csvFile': forms.ClearableFileInput(attrs={'class': 'w3-button w3-white w3-border w3-border-red w3-round-large'}),
        }