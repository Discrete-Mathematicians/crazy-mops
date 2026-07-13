from django.db import IntegrityError, transaction
from django.test import TestCase

from pets.models import Pet
from subscriptions.models import Subscription
from users.models import User


class SubscriptionModelCreationTests(TestCase):
    """Создание модели Subscription и сохранение в БД."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")
        self.subscriber = User.objects.create_user(login="subscriber", password="testpass123")
        self.pet = Pet.objects.create(owner=self.owner, name="Barsik")

    def test_create_subscription_saves_to_database(self):
        subscription = Subscription.objects.create(user=self.subscriber, pet=self.pet)

        actual = Subscription.objects.filter(pk=subscription.pk).exists()

        self.assertTrue(actual)

    def test_str_representation(self):
        subscription = Subscription.objects.create(user=self.subscriber, pet=self.pet)

        actual = str(subscription)

        self.assertEqual(actual, f"{self.subscriber} → {self.pet}")


class SubscriptionUniqueConstraintTests(TestCase):
    """Уникальность пары user+pet."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")
        self.subscriber = User.objects.create_user(login="subscriber", password="testpass123")
        self.pet = Pet.objects.create(owner=self.owner, name="Barsik")

    def test_duplicate_user_pet_pair_raises_integrity_error(self):
        Subscription.objects.create(user=self.subscriber, pet=self.pet)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Subscription.objects.create(user=self.subscriber, pet=self.pet)

    def test_same_user_different_pets_is_allowed(self):
        other_pet = Pet.objects.create(owner=self.owner, name="Rex")
        Subscription.objects.create(user=self.subscriber, pet=self.pet)

        Subscription.objects.create(user=self.subscriber, pet=other_pet)

        actual = Subscription.objects.filter(user=self.subscriber).count()
        self.assertEqual(actual, 2)

    def test_same_pet_different_users_is_allowed(self):
        other_subscriber = User.objects.create_user(login="subscriber2", password="testpass123")
        Subscription.objects.create(user=self.subscriber, pet=self.pet)

        Subscription.objects.create(user=other_subscriber, pet=self.pet)

        actual = Subscription.objects.filter(pet=self.pet).count()
        self.assertEqual(actual, 2)
