from django import forms
from django.forms import ModelForm

from . models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'objet', 'phone', 'descr']

        widgets={
            'name' : forms.TextInput(),
            'email' : forms.EmailInput(),
            'phone' : forms.TextInput(),
            'objet' : forms.TextInput(),
            'descr' : forms.Textarea()
        }