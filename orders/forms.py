from django import forms

class CartAddBookForm(forms.Form):
    units = forms.IntegerField(min_value=1,
        max_value=20)