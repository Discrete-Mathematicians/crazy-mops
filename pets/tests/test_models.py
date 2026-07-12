from django.test import TestCase

from pets.models import Pet
from users.models import User


class PetModelCreationTests(TestCase):
    """Создание модели Pet и сохранение в БД."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")

    def test_create_pet_saves_to_database(self):
        pet = Pet.objects.create(owner=self.owner, name="Barsik")

        actual = Pet.objects.filter(pk=pet.pk).exists()

        self.assertTrue(actual)

    def test_create_pet_sets_default_pet_type(self):
        pet = Pet.objects.create(owner=self.owner, name="Barsik")

        actual = pet.pet_type

        self.assertEqual(actual, Pet.PetType.OTHER)


class PetModelStrTests(TestCase):
    """Метод __str__ модели Pet."""

    def test_str_returns_name(self):
        owner = User.objects.create_user(login="owner", password="testpass123")
        pet = Pet.objects.create(owner=owner, name="Barsik")

        actual = str(pet)

        self.assertEqual(actual, "Barsik")
