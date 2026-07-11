from django.test import TestCase

from users.forms import ProfileEditForm, SignUpForm
from users.models import User


class SignUpFormValidationTests(TestCase):
    """Валидация формы регистрации SignUpForm."""

    def test_valid_data_is_accepted(self):
        form = SignUpForm(data={"login": "catlover", "password1": "supersecret123", "password2": "supersecret123"})

        actual = form.is_valid()

        self.assertTrue(actual)

    def test_missing_login_is_rejected(self):
        form = SignUpForm(data={"login": "", "password1": "supersecret123", "password2": "supersecret123"})

        actual = form.is_valid()

        self.assertFalse(actual)

    def test_mismatched_passwords_are_rejected(self):
        form = SignUpForm(data={"login": "catlover", "password1": "supersecret123", "password2": "otherpassword456"})

        actual = form.is_valid()

        self.assertFalse(actual)

    def test_too_common_password_is_rejected(self):
        form = SignUpForm(data={"login": "catlover", "password1": "password", "password2": "password"})

        actual = form.is_valid()

        self.assertFalse(actual)

    def test_duplicate_login_is_rejected(self):
        User.objects.create_user(login="catlover", password="supersecret123")

        form = SignUpForm(data={"login": "catlover", "password1": "anotherpass456", "password2": "anotherpass456"})

        actual = form.is_valid()

        self.assertFalse(actual)

    def test_valid_data_creates_user(self):
        form = SignUpForm(data={"login": "catlover", "password1": "supersecret123", "password2": "supersecret123"})
        form.is_valid()

        user = form.save()

        actual = User.objects.filter(pk=user.pk).exists()
        self.assertTrue(actual)


class ProfileEditFormTests(TestCase):
    """Форма редактирования профиля ProfileEditForm."""

    def setUp(self):
        self.user = User.objects.create_user(login="catlover", password="supersecret123")

    def test_has_no_password_field(self):
        form = ProfileEditForm(instance=self.user)

        actual = "password" in form.fields

        self.assertFalse(actual)

    def test_valid_data_updates_display_name(self):
        form = ProfileEditForm(
            data={"display_name": "Мурзик", "first_name": "", "last_name": "", "email": ""},
            instance=self.user,
        )
        form.is_valid()

        form.save()

        actual = User.objects.get(pk=self.user.pk).display_name
        self.assertEqual(actual, "Мурзик")

    def test_invalid_email_is_rejected(self):
        form = ProfileEditForm(
            data={"display_name": "Мурзик", "first_name": "", "last_name": "", "email": "not-an-email"},
            instance=self.user,
        )

        actual = form.is_valid()

        self.assertFalse(actual)
