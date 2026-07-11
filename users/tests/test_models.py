from django.db.utils import IntegrityError
from django.test import TestCase

from users.models import User


class UserModelCreationTests(TestCase):
    """Создание модели User и сохранение в БД."""

    def test_create_user_saves_to_database(self):
        user = User.objects.create_user(login="catlover", password="supersecret123")

        actual = User.objects.filter(pk=user.pk).exists()

        self.assertTrue(actual)

    def test_create_user_hashes_password(self):
        user = User.objects.create_user(login="doglover", password="supersecret123")

        actual = user.password

        self.assertNotEqual(actual, "supersecret123")

    def test_create_user_sets_default_account_type(self):
        user = User.objects.create_user(login="birdlover", password="supersecret123")

        actual = user.account_type

        self.assertEqual(actual, User.AccountType.USER)

    def test_create_user_without_login_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(login="", password="supersecret123")

    def test_create_user_with_duplicate_login_raises_error(self):
        User.objects.create_user(login="catlover", password="supersecret123")

        with self.assertRaises(IntegrityError):
            User.objects.create_user(login="catlover", password="anotherpass123")

    def test_create_superuser_sets_staff_and_superuser_flags(self):
        user = User.objects.create_superuser(login="admin", password="supersecret123")

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class UserModelStrTests(TestCase):
    """Метод __str__ модели User."""

    def test_str_returns_display_name_when_set(self):
        user = User.objects.create_user(login="catlover", password="supersecret123", display_name="Мурзик")

        actual = str(user)

        self.assertEqual(actual, "Мурзик")

    def test_str_falls_back_to_login_when_display_name_empty(self):
        user = User.objects.create_user(login="catlover", password="supersecret123")

        actual = str(user)

        self.assertEqual(actual, "catlover")


class UserModelSaveTests(TestCase):
    """Поведение save() модели User."""

    def test_save_sets_display_name_to_login_when_blank(self):
        user = User(login="catlover")
        user.set_password("supersecret123")

        user.save()

        actual = user.display_name
        self.assertEqual(actual, "catlover")

    def test_save_keeps_custom_display_name(self):
        user = User(login="catlover", display_name="Мурзик")
        user.set_password("supersecret123")

        user.save()

        actual = user.display_name
        self.assertEqual(actual, "Мурзик")


class UserModelAvatarUrlTests(TestCase):
    """Свойство avatar_url модели User."""

    def test_avatar_url_returns_default_when_no_avatar(self):
        user = User.objects.create_user(login="catlover", password="supersecret123")

        actual = user.avatar_url

        self.assertIn("default_avatar.png", actual)
