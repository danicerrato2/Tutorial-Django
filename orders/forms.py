from django import forms
from .models import Order


class CartAddBookForm(forms.Form):

    quantity = forms.TypedChoiceField(
        coerce=int,
        choices=[(x, x) for x in range(1, 21)],
        required=True
    )


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email',
            'address', 'postal_code', 'city',
            ]
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'id': 'first_name',
                    'placeholder': 'First Name'
                    }
                ),
            'last_name': forms.TextInput(
                attrs={
                    'id': 'last_name',
                    'placeholder': 'Last Name'
                    }
                ),
            'email': forms.EmailInput(
                attrs={
                    'id': 'email',
                    'placeholder': 'Email'
                    }
                ),
            'address': forms.TextInput(
                attrs={
                    'id': 'address',
                    'placeholder': 'Address'
                    }
                ),
            'postal_code': forms.TextInput(
                attrs={
                    'id': 'postal_code',
                    'placeholder': 'Postal Code'
                    }
                ),
            'city': forms.TextInput(
                attrs={
                    'id': 'city',
                    'placeholder': 'City'
                    }
                ),
            }