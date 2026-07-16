from django.test import TestCase
from django.urls import reverse

from pets.models import Pet
from users.models import User


class ProfileDetailAccessTests(TestCase):
    """Доступность страницы профиля и обработка несуществующего юзера."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")

    def test_get_returns_200_for_guest(self):
        response = self.client.get(reverse("profiles:detail", args=[self.owner.pk]))

        actual = response.status_code
        self.assertEqual(actual, 200)

    def test_nonexistent_user_returns_404(self):
        response = self.client.get(reverse("profiles:detail", args=[999999]))

        actual = response.status_code
        self.assertEqual(actual, 404)


class ProfilePetsListTests(TestCase):
    """Список питомцев на странице профиля."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")

    def test_pets_context_matches_owners_pets(self):
        own_pet = Pet.objects.create(owner=self.owner, name="Barsik")
        other_user = User.objects.create_user(login="other", password="testpass123")
        Pet.objects.create(owner=other_user, name="Rex")

        response = self.client.get(reverse("profiles:detail", args=[self.owner.pk]))

        actual = list(response.context["pets"])
        self.assertEqual(actual, [own_pet])

    def test_no_pets_returns_empty_list(self):
        response = self.client.get(reverse("profiles:detail", args=[self.owner.pk]))

        actual = list(response.context["pets"])
        self.assertEqual(actual, [])


class ProfileCanManageTests(TestCase):
    """Флаг can_manage: кто видит владельческие кнопки."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")

    def get_can_manage(self):
        response = self.client.get(reverse("profiles:detail", args=[self.owner.pk]))
        return response.context["can_manage"]

    def test_can_manage_true_for_owner(self):
        self.client.login(login="owner", password="testpass123")

        actual = self.get_can_manage()

        self.assertTrue(actual)

    def test_can_manage_true_for_staff_admin(self):
        User.objects.create_user(login="admin1", password="testpass123", is_staff=True)
        self.client.login(login="admin1", password="testpass123")

        actual = self.get_can_manage()

        self.assertTrue(actual)

    def test_can_manage_false_for_other_user(self):
        User.objects.create_user(login="other2", password="testpass123")
        self.client.login(login="other2", password="testpass123")

        actual = self.get_can_manage()

        self.assertFalse(actual)

    def test_can_manage_false_for_anonymous(self):
        actual = self.get_can_manage()

        self.assertFalse(actual)

    def test_edit_button_visible_for_owner(self):
        self.client.login(login="owner", password="testpass123")

        response = self.client.get(reverse("profiles:detail", args=[self.owner.pk]))

        self.assertContains(response, "Редактировать")

    def test_edit_button_hidden_for_anonymous(self):
        response = self.client.get(reverse("profiles:detail", args=[self.owner.pk]))

        self.assertNotContains(response, "Редактировать")
