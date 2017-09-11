""" forms.py """
from django import forms
from .models import Store_item_request

class StoreItemRequestForm(forms.ModelForm):
    """ Form to request a new store item """

    
    class Meta:
        model = Store_item_request
        exclude = ('child',)
