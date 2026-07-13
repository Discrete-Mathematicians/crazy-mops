from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from pets.models import Pet
from posts.models import Post
from subscriptions.models import Subscription
from users.models import User


class FeedAccessTests(TestCase):
    """Доступ к ленте."""

    def test_anonymous_redirects_to_login(self):
        response = self.client.get(reverse("feed:home"))

        expected = f"{reverse('users:login')}?next={reverse('feed:home')}"
        self.assertRedirects(response, expected)


class FeedContentTests(TestCase):
    """Содержимое ленты: только подписки, сортировка."""

    def setUp(self):
        self.viewer = User.objects.create_user(login="viewer", password="testpass123")
        owner = User.objects.create_user(login="owner", password="testpass123")
        self.subscribed_pet = Pet.objects.create(owner=owner, name="Barsik")
        self.other_pet = Pet.objects.create(owner=owner, name="Rex")
        Subscription.objects.create(user=self.viewer, pet=self.subscribed_pet)
        self.client.login(login="viewer", password="testpass123")

    def test_shows_only_posts_from_subscribed_pets(self):
        subscribed_post = Post.objects.create(pet=self.subscribed_pet, title="Прогулка")
        Post.objects.create(pet=self.other_pet, title="Не моё")

        response = self.client.get(reverse("feed:home"))

        actual = list(response.context["posts"])
        self.assertEqual(actual, [subscribed_post])

    def test_posts_sorted_by_created_at_descending(self):
        older = Post.objects.create(pet=self.subscribed_pet, title="Старый")
        Post.objects.filter(pk=older.pk).update(created_at=timezone.now() - timedelta(days=1))
        newer = Post.objects.create(pet=self.subscribed_pet, title="Новый")

        response = self.client.get(reverse("feed:home"))

        actual = list(response.context["posts"])
        self.assertEqual(actual, [newer, older])

    def test_empty_feed_shows_empty_posts_list(self):
        response = self.client.get(reverse("feed:home"))

        actual = list(response.context["posts"])
        self.assertEqual(actual, [])

    def test_empty_feed_shows_find_pets_link(self):
        response = self.client.get(reverse("feed:home"))

        self.assertContains(response, "Найти питомцев")


class FeedPaginationTests(TestCase):
    """Пагинация ленты (10 постов на страницу)."""

    def setUp(self):
        self.viewer = User.objects.create_user(login="viewer", password="testpass123")
        owner = User.objects.create_user(login="owner", password="testpass123")
        pet = Pet.objects.create(owner=owner, name="Barsik")
        Subscription.objects.create(user=self.viewer, pet=pet)
        for i in range(11):
            Post.objects.create(pet=pet, title=f"Пост {i}")
        self.client.login(login="viewer", password="testpass123")

    def test_first_page_has_ten_posts(self):
        response = self.client.get(reverse("feed:home"))

        actual = len(response.context["posts"])
        self.assertEqual(actual, 10)

    def test_first_page_is_paginated(self):
        response = self.client.get(reverse("feed:home"))

        actual = response.context["is_paginated"]
        self.assertTrue(actual)

    def test_second_page_has_remaining_post(self):
        response = self.client.get(reverse("feed:home"), {"page": 2})

        actual = len(response.context["posts"])
        self.assertEqual(actual, 1)
