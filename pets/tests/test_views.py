from django.test import TestCase
from django.urls import reverse

from pets.models import Pet
from users.models import User


class PetDetailViewTests(TestCase):
    """Просмотр карточки питомца."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")
        self.pet = Pet.objects.create(owner=self.owner, name="Barsik")

    def test_detail_accessible_to_guest(self):
        response = self.client.get(reverse("pets:detail", args=[self.pet.pk]))

        actual = response.status_code
        self.assertEqual(actual, 200)


class PetCreateViewTests(TestCase):
    """Создание карточки питомца."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")

    def test_get_form_returns_200_for_authenticated_user(self):
        self.client.login(login="owner", password="testpass123")

        response = self.client.get(reverse("pets:create"))

        actual = response.status_code
        self.assertEqual(actual, 200)

    def test_post_valid_data_creates_pet(self):
        self.client.login(login="owner", password="testpass123")

        self.client.post(reverse("pets:create"), data={"name": "Barsik", "pet_type": "dog"})

        actual = Pet.objects.filter(name="Barsik").exists()
        self.assertTrue(actual)

    def test_post_valid_data_sets_owner_to_current_user(self):
        self.client.login(login="owner", password="testpass123")

        self.client.post(reverse("pets:create"), data={"name": "Barsik", "pet_type": "dog"})

        actual = Pet.objects.get(name="Barsik").owner
        self.assertEqual(actual, self.owner)

    def test_post_valid_data_redirects_to_detail(self):
        self.client.login(login="owner", password="testpass123")

        response = self.client.post(reverse("pets:create"), data={"name": "Barsik", "pet_type": "dog"})

        pet = Pet.objects.get(name="Barsik")
        self.assertRedirects(response, reverse("pets:detail", args=[pet.pk]))

    def test_post_blank_name_does_not_create_pet(self):
        self.client.login(login="owner", password="testpass123")

        self.client.post(reverse("pets:create"), data={"name": "   ", "pet_type": "dog"})

        actual = Pet.objects.exists()
        self.assertFalse(actual)

    def test_post_blank_name_returns_200_with_errors(self):
        self.client.login(login="owner", password="testpass123")

        response = self.client.post(reverse("pets:create"), data={"name": "   ", "pet_type": "dog"})

        actual = response.status_code
        self.assertEqual(actual, 200)
        self.assertTrue(response.context["form"].errors)

    def test_anonymous_get_redirects_to_login(self):
        response = self.client.get(reverse("pets:create"))

        expected = f"{reverse('users:login')}?next={reverse('pets:create')}"
        self.assertRedirects(response, expected)

    def test_anonymous_post_creates_no_pet(self):
        self.client.post(reverse("pets:create"), data={"name": "Barsik", "pet_type": "dog"})

        actual = Pet.objects.exists()
        self.assertFalse(actual)


class PetUpdateViewTests(TestCase):
    """Редактирование карточки питомца."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")
        self.other_user = User.objects.create_user(login="other", password="testpass123")
        self.pet = Pet.objects.create(owner=self.owner, name="Barsik", pet_type=Pet.PetType.DOG)

    def test_get_form_returns_200_for_owner(self):
        self.client.login(login="owner", password="testpass123")

        response = self.client.get(reverse("pets:edit", args=[self.pet.pk]))

        actual = response.status_code
        self.assertEqual(actual, 200)

    def test_post_valid_data_updates_pet(self):
        self.client.login(login="owner", password="testpass123")

        self.client.post(reverse("pets:edit", args=[self.pet.pk]), data={"name": "Rex", "pet_type": "dog"})

        actual = Pet.objects.get(pk=self.pet.pk).name
        self.assertEqual(actual, "Rex")

    def test_post_valid_data_redirects_to_detail(self):
        self.client.login(login="owner", password="testpass123")

        response = self.client.post(reverse("pets:edit", args=[self.pet.pk]), data={"name": "Rex", "pet_type": "dog"})

        self.assertRedirects(response, reverse("pets:detail", args=[self.pet.pk]))

    def test_post_blank_name_does_not_update_pet(self):
        self.client.login(login="owner", password="testpass123")

        self.client.post(reverse("pets:edit", args=[self.pet.pk]), data={"name": "   ", "pet_type": "dog"})

        actual = Pet.objects.get(pk=self.pet.pk).name
        self.assertEqual(actual, "Barsik")

    def test_other_authenticated_user_gets_403(self):
        self.client.login(login="other", password="testpass123")

        response = self.client.get(reverse("pets:edit", args=[self.pet.pk]))

        actual = response.status_code
        self.assertEqual(actual, 403)

    def test_other_authenticated_user_cannot_update_pet(self):
        self.client.login(login="other", password="testpass123")

        self.client.post(reverse("pets:edit", args=[self.pet.pk]), data={"name": "Rex", "pet_type": "dog"})

        actual = Pet.objects.get(pk=self.pet.pk).name
        self.assertEqual(actual, "Barsik")

    def test_anonymous_redirects_to_login(self):
        response = self.client.get(reverse("pets:edit", args=[self.pet.pk]))

        expected = f"{reverse('users:login')}?next={reverse('pets:edit', args=[self.pet.pk])}"
        self.assertRedirects(response, expected)


class PetDeleteViewTests(TestCase):
    """Удаление карточки питомца."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")
        self.other_user = User.objects.create_user(login="other", password="testpass123")
        self.pet = Pet.objects.create(owner=self.owner, name="Barsik")

    def test_post_delete_removes_pet(self):
        self.client.login(login="owner", password="testpass123")

        self.client.post(reverse("pets:delete", args=[self.pet.pk]))

        actual = Pet.objects.filter(pk=self.pet.pk).exists()
        self.assertFalse(actual)

    def test_post_delete_redirects_to_create_page(self):
        self.client.login(login="owner", password="testpass123")

        response = self.client.post(reverse("pets:delete", args=[self.pet.pk]))

        self.assertRedirects(response, reverse("pets:create"))

    def test_other_authenticated_user_gets_403(self):
        self.client.login(login="other", password="testpass123")

        response = self.client.post(reverse("pets:delete", args=[self.pet.pk]))

        actual = response.status_code
        self.assertEqual(actual, 403)

    def test_other_authenticated_user_cannot_delete_pet(self):
        self.client.login(login="other", password="testpass123")

        self.client.post(reverse("pets:delete", args=[self.pet.pk]))

        actual = Pet.objects.filter(pk=self.pet.pk).exists()
        self.assertTrue(actual)

    def test_anonymous_redirects_to_login(self):
        response = self.client.get(reverse("pets:delete", args=[self.pet.pk]))

        expected = f"{reverse('users:login')}?next={reverse('pets:delete', args=[self.pet.pk])}"
        self.assertRedirects(response, expected)

    def test_anonymous_cannot_delete_pet(self):
        self.client.post(reverse("pets:delete", args=[self.pet.pk]))

        actual = Pet.objects.filter(pk=self.pet.pk).exists()
        self.assertTrue(actual)
