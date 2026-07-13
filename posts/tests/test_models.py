from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.test import TestCase

from pets.models import Pet
from posts.models import Post, PostMedia, PostTag, Tag
from users.models import User


class PostModelTests(TestCase):
    """Создание модели Post и сохранение в БД."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")
        self.pet = Pet.objects.create(owner=self.owner, name="Barsik")

    def test_create_post_saves_to_database(self):
        post = Post.objects.create(pet=self.pet, title="Прогулка")

        actual = Post.objects.filter(pk=post.pk).exists()

        self.assertTrue(actual)

    def test_str_returns_pet_name_and_title(self):
        post = Post.objects.create(pet=self.pet, title="Прогулка")

        actual = str(post)

        self.assertEqual(actual, "Barsik: Прогулка")


class TagModelTests(TestCase):
    """Метод __str__ модели Tag."""

    def test_str_returns_name(self):
        tag = Tag.objects.create(name="прогулка")

        actual = str(tag)

        self.assertEqual(actual, "прогулка")


class PostTagModelTests(TestCase):
    """Создание модели PostTag и уникальность пары post+tag."""

    def setUp(self):
        owner = User.objects.create_user(login="owner", password="testpass123")
        pet = Pet.objects.create(owner=owner, name="Barsik")
        self.post = Post.objects.create(pet=pet, title="Прогулка")
        self.tag = Tag.objects.create(name="прогулка")

    def test_create_post_tag_saves_to_database(self):
        post_tag = PostTag.objects.create(post=self.post, tag=self.tag)

        actual = PostTag.objects.filter(pk=post_tag.pk).exists()

        self.assertTrue(actual)

    def test_str_format(self):
        post_tag = PostTag.objects.create(post=self.post, tag=self.tag)

        actual = str(post_tag)

        self.assertEqual(actual, f"{self.post.pk} - прогулка")

    def test_duplicate_post_tag_pair_raises_integrity_error(self):
        PostTag.objects.create(post=self.post, tag=self.tag)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                PostTag.objects.create(post=self.post, tag=self.tag)


class PostMediaModelTests(TestCase):
    """Создание модели PostMedia и дефолтные значения."""

    def setUp(self):
        owner = User.objects.create_user(login="owner", password="testpass123")
        pet = Pet.objects.create(owner=owner, name="Barsik")
        self.post = Post.objects.create(pet=pet, title="Прогулка")

    def make_file(self, name="photo.jpg"):
        return SimpleUploadedFile(name, b"content", content_type="image/jpeg")

    def test_create_post_media_saves_to_database(self):
        media = PostMedia.objects.create(post=self.post, media_url=self.make_file())

        actual = PostMedia.objects.filter(pk=media.pk).exists()

        self.assertTrue(actual)

    def test_default_media_type_is_image(self):
        media = PostMedia.objects.create(post=self.post, media_url=self.make_file())

        actual = media.media_type

        self.assertEqual(actual, PostMedia.MediaType.IMAGE)

    def test_str_format(self):
        media = PostMedia.objects.create(post=self.post, media_url=self.make_file("photo.jpg"))

        actual = str(media)

        self.assertEqual(actual, f"{self.post.pk}: {media.media_url.name}")
