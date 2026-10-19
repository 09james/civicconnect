"""Forms for citizen registration."""

import secrets

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class CitizenRegistrationForm(UserCreationForm):
    """Registration form that always creates a citizen account."""

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CITIZEN
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user


class InitialAdminSetupForm(UserCreationForm):
    """Create the first superuser when presented with the deployment token."""

    bootstrap_token = forms.CharField(
        label="One-time setup token",
        widget=forms.PasswordInput,
        max_length=256,
        strip=False,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, expected_token, **kwargs):
        self.expected_token = expected_token
        super().__init__(*args, **kwargs)

    def clean_bootstrap_token(self):
        token = self.cleaned_data["bootstrap_token"]
        if not secrets.compare_digest(token, self.expected_token):
            raise forms.ValidationError("The setup token is not valid.")
        return token

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.ADMIN
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user
