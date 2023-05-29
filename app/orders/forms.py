from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """Form for Orders"""

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Marty',
        }),
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'McFly',
        }),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'back_to_the_future_2015@example.com',
            },
        ),
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'USA, California, Hill Valley',
        }),
    )
