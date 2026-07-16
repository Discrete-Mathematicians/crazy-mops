from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    """Регистрация: обязательны только login + password (password1/password2)."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("login",)


class ProfileEditForm(UserChangeForm):
    password = None  # чтобы хеш пароля не торчал в форме

    class Meta:
        model = User
        fields = ("display_name", "first_name", "last_name", "email", "avatar", "pronouns", "gender", "city", "info")
