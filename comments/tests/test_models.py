from django.test import TestCase

from comments.models import Comment, CommentMedia
from pets.models import Pet
from posts.models import Post
from users.models import User


class CommentModelTests(TestCase):
    """Создание модели Comment, __str__, reply_comment."""

    def setUp(self):
        owner = User.objects.create_user(login="owner", password="testpass123")
        pet = Pet.objects.create(owner=owner, name="Barsik")
        self.post = Post.objects.create(pet=pet, title="Прогулка")
        self.author = User.objects.create_user(login="author", password="testpass123")

    def test_create_comment_saves_to_database(self):
        comment = Comment.objects.create(post=self.post, user=self.author, description="Милота!")

        actual = Comment.objects.filter(pk=comment.pk).exists()

        self.assertTrue(actual)

    def test_str_returns_author_and_description_prefix(self):
        comment = Comment.objects.create(post=self.post, user=self.author, description="А" * 40)

        actual = str(comment)

        self.assertEqual(actual, f"{self.author}: {'А' * 30}")

    def test_reply_comment_defaults_to_none(self):
        comment = Comment.objects.create(post=self.post, user=self.author, description="Милота!")

        actual = comment.reply_comment

        self.assertIsNone(actual)

    def test_reply_comment_links_to_parent(self):
        parent = Comment.objects.create(post=self.post, user=self.author, description="Родитель")

        reply = Comment.objects.create(post=self.post, user=self.author, description="Ответ", reply_comment=parent)

        actual = reply.reply_comment
        self.assertEqual(actual, parent)

    def test_parent_replies_includes_reply(self):
        parent = Comment.objects.create(post=self.post, user=self.author, description="Родитель")
        reply = Comment.objects.create(post=self.post, user=self.author, description="Ответ", reply_comment=parent)

        actual = list(parent.replies.all())

        self.assertEqual(actual, [reply])


class CommentMediaModelTests(TestCase):
    """Создание модели CommentMedia."""

    def setUp(self):
        owner = User.objects.create_user(login="owner", password="testpass123")
        pet = Pet.objects.create(owner=owner, name="Barsik")
        post = Post.objects.create(pet=pet, title="Прогулка")
        author = User.objects.create_user(login="author", password="testpass123")
        self.comment = Comment.objects.create(post=post, user=author, description="Милота!")

    def test_create_saves_to_database(self):
        media = CommentMedia.objects.create(
            comment=self.comment, media_url="comment_media/photo.jpg", media_type=CommentMedia.IMAGE
        )

        actual = CommentMedia.objects.filter(pk=media.pk).exists()

        self.assertTrue(actual)

    def test_str_format(self):
        media = CommentMedia.objects.create(
            comment=self.comment, media_url="comment_media/photo.jpg", media_type=CommentMedia.IMAGE
        )

        actual = str(media)

        self.assertEqual(actual, f"Медиа #{media.pk} к комментарию #{self.comment.pk}")
