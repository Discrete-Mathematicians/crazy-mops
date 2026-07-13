from django.test import TestCase
from django.urls import reverse

from pets.models import Pet
from posts.models import Post, Tag
from users.models import User


class PostTagSavingTests(TestCase):
    """Сохранение тегов через форму создания/редактирования поста."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")
        self.pet = Pet.objects.create(owner=self.owner, name="Barsik")
        self.client.login(login="owner", password="testpass123")

    def test_create_with_tags_creates_tag_objects(self):
        self.client.post(
            reverse("posts:create", args=[self.pet.pk]),
            data={"title": "Прогулка", "description": "", "tags": "#Парк, Гуляем"},
        )

        post = Post.objects.get(title="Прогулка")
        actual = set(post.tags.values_list("name", flat=True))
        self.assertEqual(actual, {"парк", "гуляем"})

    def test_create_reuses_existing_tag_instead_of_duplicating(self):
        Tag.objects.create(name="парк")

        self.client.post(
            reverse("posts:create", args=[self.pet.pk]),
            data={"title": "Прогулка", "description": "", "tags": "парк"},
        )

        actual = Tag.objects.filter(name="парк").count()
        self.assertEqual(actual, 1)

    def test_edit_replaces_tags_completely(self):
        post = Post.objects.create(pet=self.pet, title="Прогулка")
        post.tags.set([Tag.objects.create(name="старый")])

        self.client.post(
            reverse("posts:edit", args=[post.pk]),
            data={"title": "Прогулка", "description": "", "tags": "новый"},
        )

        actual = set(Post.objects.get(pk=post.pk).tags.values_list("name", flat=True))
        self.assertEqual(actual, {"новый"})
