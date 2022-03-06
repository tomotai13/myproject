from django import forms

class UrlForm(forms.Form):
    url = forms.CharField(min_length=10, max_length=100, label=False, 
    widget=forms.TextInput(
        attrs={
            'placeholder':'enter-url',
            'class':'form-control',
            'id':'exampleFormControlInput1',
            }))