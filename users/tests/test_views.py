from django.test import TestCase
from django.urls import reverse

from users.models import User


class SignupViewTests(TestCase):
    """Регистрация пользователя через users:signup."""

    def test_get_returns_200(self):
        response = self.client.get(reverse("users:signup"))

        actual = response.status_code
        self.assertEqual(actual, 200)

    def test_post_valid_data_creates_user(self):
        self.client.post(
            reverse("users:signup"),
            data={"login": "catlover", "password1": "supersecret123", "password2": "supersecret123"},
        )

        actual = User.objects.filter(login="catlover").exists()
        self.assertTrue(actual)

    def test_post_valid_data_logs_user_in(self):
        self.client.post(
            reverse("users:signup"),
            data={"login": "catlover", "password1": "supersecret123", "password2": "supersecret123"},
        )

        actual = self.client.session.get("_auth_user_id")
        self.assertIsNotNone(actual)

    def test_post_valid_data_redirects_to_profile_edit(self):
        response = self.client.post(
            reverse("users:signup"),
            data={"login": "catlover", "password1": "supersecret123", "password2": "supersecret123"},
        )

        self.assertRedirects(response, reverse("users:profile_edit"))

    def test_post_invalid_data_does_not_create_user(self):
        self.client.post(
            reverse("users:signup"),
            data={"login": "catlover", "password1": "supersecret123", "password2": "mismatch456"},
        )

        actual = User.objects.filter(login="catlover").exists()
        self.assertFalse(actual)

    def test_post_invalid_data_returns_200_with_errors(self):
        response = self.client.post(
            reverse("users:signup"),
            data={"login": "catlover", "password1": "supersecret123", "password2": "mismatch456"},
        )

        actual = response.status_code
        self.assertEqual(actual, 200)
        self.assertTrue(response.context["form"].errors)


class LoginViewTests(TestCase):
    """Логин пользователя через users:login."""

    def setUp(self):
        self.user = User.objects.create_user(login="catlover", password="supersecret123")

    def test_get_returns_200(self):
        response = self.client.get(reverse("users:login"))

        actual = response.status_code
        self.assertEqual(actual, 200)

    def test_post_valid_credentials_logs_in(self):
        self.client.post(reverse("users:login"), data={"username": "catlover", "password": "supersecret123"})

        actual = self.client.session.get("_auth_user_id")
        self.assertEqual(actual, str(self.user.pk))

    def test_post_invalid_credentials_does_not_log_in(self):
        self.client.post(reverse("users:login"), data={"username": "catlover", "password": "wrongpassword"})

        actual = self.client.session.get("_auth_user_id")
        self.assertIsNone(actual)

    def test_post_invalid_credentials_returns_200_with_error(self):
        response = self.client.post(reverse("users:login"), data={"username": "catlover", "password": "wrongpassword"})

        actual = response.status_code
        self.assertEqual(actual, 200)
        self.assertTrue(response.context["form"].errors)


class LogoutViewTests(TestCase):
    """Логаут пользователя через users:logout."""

    def test_logout_clears_session(self):
        User.objects.create_user(login="catlover", password="supersecret123")
        self.client.login(login="catlover", password="supersecret123")

        self.client.post(reverse("users:logout"))

        actual = self.client.session.get("_auth_user_id")
        self.assertIsNone(actual)


class ProfileEditAccessTests(TestCase):
    """Доступ к users:profile_edit без логина и с логином."""

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse("users:profile_edit"))

        expected = f"{reverse('users:login')}?next={reverse('users:profile_edit')}"
        self.assertRedirects(response, expected)

    def test_authenticated_user_gets_200(self):
        User.objects.create_user(login="catlover", password="supersecret123")
        self.client.login(login="catlover", password="supersecret123")

        response = self.client.get(reverse("users:profile_edit"))

        actual = response.status_code
        self.assertEqual(actual, 200)

    def test_authenticated_user_can_update_profile(self):
        user = User.objects.create_user(login="catlover", password="supersecret123")
        self.client.login(login="catlover", password="supersecret123")

        response = self.client.post(
            reverse("users:profile_edit"),
            data={"display_name": "Мурзик", "first_name": "", "last_name": "", "email": ""},
        )

        self.assertRedirects(response, reverse("users:profile_edit"))
        actual = User.objects.get(pk=user.pk).display_name
        self.assertEqual(actual, "Мурзик")
