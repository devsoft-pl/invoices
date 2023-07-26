from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm as BaseUserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("password"),
        help_text=_("Hasło jest szyfrowane, więc nie można je zobaczyć."),
    )

    class Meta:
        model = User
        fields = ["username", "password", "email"]


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email"]
