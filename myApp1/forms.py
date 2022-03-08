from django import forms


class BurgerForm(forms.Form):
    name = forms.CharField(help_text='Fill your name here')
    topping1 = forms.CharField(label='Topping 1', max_length=100)
    topping2 = forms.CharField(label='Topping 1', max_length=100, widget=forms.TextInput(attrs={'size': 3}))
    type = forms.ChoiceField(label='Type', choices=[('Sandwich', 'Sandwich'), ('Combo', 'Combo')])
