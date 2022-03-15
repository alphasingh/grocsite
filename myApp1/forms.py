from django import forms
from .models import Burger


class BurgerForm(forms.ModelForm):
    class Meta:
        model = Burger
        fields = ['topping1', 'topping2', 'kind']
