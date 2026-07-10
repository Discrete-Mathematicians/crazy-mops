from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "login", "email", "display_name")


class ProfileEditForm(UserChangeForm):
    password = None  # чтобы хеш пароля не торчал в форме

    class Meta:
        model = User
        fields = ("display_name", "avatar", "email")