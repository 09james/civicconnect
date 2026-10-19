"""Forms for citizen registration."""

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
