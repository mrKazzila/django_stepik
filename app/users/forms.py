from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from .models import User
from .tasks import send_email_verification


class UserLoginForm(AuthenticationForm):
    """Form for Login"""

    class Meta:
        model = User
        fields = ('username', 'password')

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Username',
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Password',
        }),
    )


class UserRegistrationForm(UserCreationForm):
    """Form for Registration"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Name',
        }),
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Surname',
        }),
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Username',
        }),
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'E-mail address',
        }),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Password',
        }),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Confirm password',
        }),
    )

    def save(self, commit=True):
        user = super().save(commit=True)
        send_email_verification.delay(user.id)
        return user


class UserProfileForm(UserChangeForm):
    """Form for User Profile"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'email', 'username')

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
            'readonly': True,
        }),
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
            'readonly': True,
        }),
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'custom-file-input'}),
        required=False,
    )
