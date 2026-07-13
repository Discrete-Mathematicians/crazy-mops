from django.test import TestCase
from django.urls import reverse

from pets.models import Pet
from subscriptions.models import Subscription
from users.models import User


class SubscribeViewTests(TestCase):
    """Подписка на питомца через subscriptions:subscribe."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")
        self.subscriber = User.objects.create_user(login="subscriber", password="testpass123")
        self.pet = Pet.objects.create(owner=self.owner, name="Barsik")

    def test_subscribe_creates_subscription(self):
        self.client.login(login="subscriber", password="testpass123")

        self.client.post(reverse("subscriptions:subscribe", args=[self.pet.pk]))

        actual = Subscription.objects.filter(user=self.subscriber, pet=self.pet).exists()
        self.assertTrue(actual)

    def test_subscribe_redirects_to_pet_detail(self):
        self.client.login(login="subscriber", password="testpass123")

        response = self.client.post(reverse("subscriptions:subscribe", args=[self.pet.pk]))

        self.assertRedirects(response, reverse("pets:detail", args=[self.pet.pk]))

    def test_subscribe_twice_does_not_create_duplicate(self):
        self.client.login(login="subscriber", password="testpass123")

        self.client.post(reverse("subscriptions:subscribe", args=[self.pet.pk]))
        self.client.post(reverse("subscriptions:subscribe", args=[self.pet.pk]))

        actual = Subscription.objects.filter(user=self.subscriber, pet=self.pet).count()
        self.assertEqual(actual, 1)

    def test_owner_subscribing_to_own_pet_is_forbidden(self):
        self.client.login(login="owner", password="testpass123")

        response = self.client.post(reverse("subscriptions:subscribe", args=[self.pet.pk]))

        actual = response.status_code
        self.assertEqual(actual, 403)

    def test_owner_subscribing_to_own_pet_creates_no_subscription(self):
        self.client.login(login="owner", password="testpass123")

        self.client.post(reverse("subscriptions:subscribe", args=[self.pet.pk]))

        actual = Subscription.objects.filter(user=self.owner, pet=self.pet).exists()
        self.assertFalse(actual)

    def test_anonymous_subscribe_redirects_to_login(self):
        response = self.client.post(reverse("subscriptions:subscribe", args=[self.pet.pk]))

        expected = f"{reverse('users:login')}?next={reverse('subscriptions:subscribe', args=[self.pet.pk])}"
        self.assertRedirects(response, expected)

    def test_anonymous_subscribe_creates_no_subscription(self):
        self.client.post(reverse("subscriptions:subscribe", args=[self.pet.pk]))

        actual = Subscription.objects.exists()
        self.assertFalse(actual)


class UnsubscribeViewTests(TestCase):
    """Отписка от питомца через subscriptions:unsubscribe."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")
        self.subscriber = User.objects.create_user(login="subscriber", password="testpass123")
        self.pet = Pet.objects.create(owner=self.owner, name="Barsik")
        Subscription.objects.create(user=self.subscriber, pet=self.pet)

    def test_unsubscribe_deletes_subscription(self):
        self.client.login(login="subscriber", password="testpass123")

        self.client.post(reverse("subscriptions:unsubscribe", args=[self.pet.pk]))

        actual = Subscription.objects.filter(user=self.subscriber, pet=self.pet).exists()
        self.assertFalse(actual)

    def test_unsubscribe_redirects_to_pet_detail(self):
        self.client.login(login="subscriber", password="testpass123")

        response = self.client.post(reverse("subscriptions:unsubscribe", args=[self.pet.pk]))

        self.assertRedirects(response, reverse("pets:detail", args=[self.pet.pk]))

    def test_anonymous_unsubscribe_redirects_to_login(self):
        response = self.client.post(reverse("subscriptions:unsubscribe", args=[self.pet.pk]))

        expected = f"{reverse('users:login')}?next={reverse('subscriptions:unsubscribe', args=[self.pet.pk])}"
        self.assertRedirects(response, expected)

    def test_anonymous_unsubscribe_does_not_delete_subscription(self):
        self.client.post(reverse("subscriptions:unsubscribe", args=[self.pet.pk]))

        actual = Subscription.objects.filter(user=self.subscriber, pet=self.pet).exists()
        self.assertTrue(actual)
