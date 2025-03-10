from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    BaseUserCreationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)

from users.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class PasswordChangeUserForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class PasswordResetUserForm(PasswordResetForm):

    class Meta:
        model = User
        fields = ["email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class PasswordResetConfirmUserForm(SetPasswordForm):

    class Meta:
        model = User
        fields = ["new_password1", "new_password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class LoginUserForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
