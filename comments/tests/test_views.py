from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from comments.models import Comment
from comments.templatetags.comment_tags import comment_item
from pets.models import Pet
from posts.models import Post
from users.models import User


class AddCommentViewTests(TestCase):
    """Создание комментария через comments:create."""

    def setUp(self):
        owner = User.objects.create_user(login="owner", password="testpass123")
        pet = Pet.objects.create(owner=owner, name="Barsik")
        self.post = Post.objects.create(pet=pet, title="Прогулка")
        self.author = User.objects.create_user(login="author", password="testpass123")
        self.client.login(login="author", password="testpass123")

    def test_valid_data_creates_comment(self):
        self.client.post(reverse("comments:create", args=[self.post.pk]), data={"description": "Милота!"})

        actual = Comment.objects.filter(post=self.post, description="Милота!").exists()
        self.assertTrue(actual)

    def test_created_comment_has_no_reply_comment(self):
        self.client.post(reverse("comments:create", args=[self.post.pk]), data={"description": "Милота!"})

        comment = Comment.objects.get(post=self.post, description="Милота!")
        actual = comment.reply_comment
        self.assertIsNone(actual)

    def test_created_comment_author_is_current_user(self):
        self.client.post(reverse("comments:create", args=[self.post.pk]), data={"description": "Милота!"})

        comment = Comment.objects.get(post=self.post, description="Милота!")
        actual = comment.user
        self.assertEqual(actual, self.author)

    def test_redirects_to_post_detail(self):
        response = self.client.post(reverse("comments:create", args=[self.post.pk]), data={"description": "Милота!"})

        self.assertRedirects(response, reverse("posts:detail", args=[self.post.pk]))

    def test_anonymous_redirects_to_login(self):
        self.client.logout()

        response = self.client.post(reverse("comments:create", args=[self.post.pk]), data={"description": "Милота!"})

        expected = f"{reverse('users:login')}?next={reverse('comments:create', args=[self.post.pk])}"
        self.assertRedirects(response, expected)

    def test_nonexistent_post_returns_404(self):
        response = self.client.post(reverse("comments:create", args=[999999]), data={"description": "Милота!"})

        actual = response.status_code
        self.assertEqual(actual, 404)

    def test_blank_description_does_not_create_comment(self):
        self.client.post(reverse("comments:create", args=[self.post.pk]), data={"description": "   "})

        actual = Comment.objects.filter(post=self.post).exists()
        self.assertFalse(actual)

    def test_saves_uploaded_media(self):
        image = SimpleUploadedFile("photo.jpg", b"content", content_type="image/jpeg")

        self.client.post(
            reverse("comments:create", args=[self.post.pk]), data={"description": "Милота!", "media": image}
        )

        comment = Comment.objects.get(post=self.post, description="Милота!")
        actual = comment.media.count()
        self.assertEqual(actual, 1)


class AddReplyViewTests(TestCase):
    """Ответ на комментарий через comments:reply."""

    def setUp(self):
        owner = User.objects.create_user(login="owner", password="testpass123")
        pet = Pet.objects.create(owner=owner, name="Barsik")
        self.post = Post.objects.create(pet=pet, title="Прогулка")
        self.author = User.objects.create_user(login="author", password="testpass123")
        self.parent = Comment.objects.create(post=self.post, user=self.author, description="Родитель")
        self.client.login(login="author", password="testpass123")

    def test_valid_data_creates_reply(self):
        self.client.post(reverse("comments:reply", args=[self.parent.pk]), data={"description": "Ответ"})

        actual = Comment.objects.filter(reply_comment=self.parent, description="Ответ").exists()
        self.assertTrue(actual)

    def test_reply_uses_parent_post(self):
        self.client.post(reverse("comments:reply", args=[self.parent.pk]), data={"description": "Ответ"})

        reply = Comment.objects.get(reply_comment=self.parent)
        actual = reply.post
        self.assertEqual(actual, self.post)

    def test_reply_to_reply_is_allowed(self):
        first_reply = Comment.objects.create(
            post=self.post, user=self.author, description="Ответ 1", reply_comment=self.parent
        )

        self.client.post(reverse("comments:reply", args=[first_reply.pk]), data={"description": "Ответ 2"})

        actual = Comment.objects.filter(reply_comment=first_reply, description="Ответ 2").exists()
        self.assertTrue(actual)

    def test_redirects_to_post_detail(self):
        response = self.client.post(reverse("comments:reply", args=[self.parent.pk]), data={"description": "Ответ"})

        self.assertRedirects(response, reverse("posts:detail", args=[self.post.pk]))

    def test_anonymous_redirects_to_login(self):
        self.client.logout()

        response = self.client.post(reverse("comments:reply", args=[self.parent.pk]), data={"description": "Ответ"})

        expected = f"{reverse('users:login')}?next={reverse('comments:reply', args=[self.parent.pk])}"
        self.assertRedirects(response, expected)

    def test_nonexistent_comment_returns_404(self):
        response = self.client.post(reverse("comments:reply", args=[999999]), data={"description": "Ответ"})

        actual = response.status_code
        self.assertEqual(actual, 404)


class DeleteCommentViewTests(TestCase):
    """Удаление комментария через comments:delete."""

    def setUp(self):
        owner = User.objects.create_user(login="owner", password="testpass123")
        pet = Pet.objects.create(owner=owner, name="Barsik")
        self.post = Post.objects.create(pet=pet, title="Прогулка")
        self.author = User.objects.create_user(login="author", password="testpass123")
        self.other_user = User.objects.create_user(login="other", password="testpass123")
        self.comment = Comment.objects.create(post=self.post, user=self.author, description="Милота!")

    def test_author_can_delete_own_comment(self):
        self.client.login(login="author", password="testpass123")

        self.client.post(reverse("comments:delete", args=[self.comment.pk]))

        actual = Comment.objects.filter(pk=self.comment.pk).exists()
        self.assertFalse(actual)

    def test_other_user_gets_403(self):
        self.client.login(login="other", password="testpass123")

        response = self.client.post(reverse("comments:delete", args=[self.comment.pk]))

        actual = response.status_code
        self.assertEqual(actual, 403)

    def test_other_user_cannot_delete_comment(self):
        self.client.login(login="other", password="testpass123")

        self.client.post(reverse("comments:delete", args=[self.comment.pk]))

        actual = Comment.objects.filter(pk=self.comment.pk).exists()
        self.assertTrue(actual)

    def test_admin_can_delete_foreign_comment(self):
        User.objects.create_user(login="admin", password="testpass123", is_staff=True)
        self.client.login(login="admin", password="testpass123")

        self.client.post(reverse("comments:delete", args=[self.comment.pk]))

        actual = Comment.objects.filter(pk=self.comment.pk).exists()
        self.assertFalse(actual)

    def test_anonymous_redirects_to_login(self):
        response = self.client.post(reverse("comments:delete", args=[self.comment.pk]))

        expected = f"{reverse('users:login')}?next={reverse('comments:delete', args=[self.comment.pk])}"
        self.assertRedirects(response, expected)

    def test_delete_redirects_to_post_detail(self):
        self.client.login(login="author", password="testpass123")

        response = self.client.post(reverse("comments:delete", args=[self.comment.pk]))

        self.assertRedirects(response, reverse("posts:detail", args=[self.post.pk]))

    def test_delete_cascades_to_replies(self):
        reply = Comment.objects.create(
            post=self.post, user=self.author, description="Ответ", reply_comment=self.comment
        )
        self.client.login(login="author", password="testpass123")

        self.client.post(reverse("comments:delete", args=[self.comment.pk]))

        actual = Comment.objects.filter(pk=reply.pk).exists()
        self.assertFalse(actual)

    def test_nonexistent_comment_returns_404(self):
        self.client.login(login="author", password="testpass123")

        response = self.client.post(reverse("comments:delete", args=[999999]))

        actual = response.status_code
        self.assertEqual(actual, 404)


class CommentDeleteButtonVisibilityTests(TestCase):
    """can_delete в инклюжн-теге comment_item: видно только автору/админу."""

    def setUp(self):
        owner = User.objects.create_user(login="owner", password="testpass123")
        pet = Pet.objects.create(owner=owner, name="Barsik")
        post = Post.objects.create(pet=pet, title="Прогулка")
        self.author = User.objects.create_user(login="author", password="testpass123")
        self.comment = Comment.objects.create(post=post, user=self.author, description="Милота!")

    def test_can_delete_true_for_author(self):
        actual = comment_item(self.comment, self.author)["can_delete"]

        self.assertTrue(actual)

    def test_can_delete_true_for_admin(self):
        admin = User.objects.create_user(login="admin", password="testpass123", is_staff=True)

        actual = comment_item(self.comment, admin)["can_delete"]

        self.assertTrue(actual)

    def test_can_delete_false_for_other_user(self):
        other_user = User.objects.create_user(login="other", password="testpass123")

        actual = comment_item(self.comment, other_user)["can_delete"]

        self.assertFalse(actual)

    def test_can_delete_false_for_anonymous(self):
        from django.contrib.auth.models import AnonymousUser

        actual = comment_item(self.comment, AnonymousUser())["can_delete"]

        self.assertFalse(actual)
