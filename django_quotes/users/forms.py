from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        min_length=3, max_length=100, required=True, widget=forms.TextInput()
    )
    email = forms.EmailField(
        min_length=3, max_length=100, required=True, widget=forms.EmailInput()
    )
    password1 = forms.CharField(
        max_length=50, required=True, widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        max_length=50, required=True, widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ["username", "password"]


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254, widget=forms.EmailInput(attrs={"placeholder": "Email"})
    )


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = self.user
        if commit:
            user.set_password(self.cleaned_data["new_password2"])
            user.save()
        return user
