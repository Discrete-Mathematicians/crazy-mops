from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from pets.models import Pet
from posts.models import Post, PostMedia
from users.models import User


class PostMediaSavingTests(TestCase):
    """Сохранение медиафайлов через форму создания/редактирования поста."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")
        self.pet = Pet.objects.create(owner=self.owner, name="Barsik")
        self.client.login(login="owner", password="testpass123")

    def image_file(self, name="photo.jpg"):
        return SimpleUploadedFile(name, b"content", content_type="image/jpeg")

    def video_file(self, name="clip.mp4"):
        return SimpleUploadedFile(name, b"content", content_type="video/mp4")

    def test_create_with_image_saves_image_media_type(self):
        self.client.post(
            reverse("posts:create", args=[self.pet.pk]),
            data={"title": "Прогулка", "description": "", "media": self.image_file()},
        )

        post = Post.objects.get(title="Прогулка")
        actual = post.media.first().media_type
        self.assertEqual(actual, PostMedia.MediaType.IMAGE)

    def test_create_with_video_saves_video_media_type(self):
        self.client.post(
            reverse("posts:create", args=[self.pet.pk]),
            data={"title": "Прогулка", "description": "", "media": self.video_file()},
        )

        post = Post.objects.get(title="Прогулка")
        actual = post.media.first().media_type
        self.assertEqual(actual, PostMedia.MediaType.VIDEO)

    def test_edit_appends_media_without_removing_existing(self):
        post = Post.objects.create(pet=self.pet, title="Прогулка")
        PostMedia.objects.create(post=post, media_url=self.image_file("old.jpg"))

        self.client.post(
            reverse("posts:edit", args=[post.pk]),
            data={"title": "Прогулка", "description": "", "media": self.image_file("new.jpg")},
        )

        actual = post.media.count()
        self.assertEqual(actual, 2)
