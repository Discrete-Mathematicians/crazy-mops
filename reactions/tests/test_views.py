from django.test import TestCase
from django.urls import reverse

from comments.models import Comment
from pets.models import Pet
from posts.models import Post
from reactions.models import Reaction
from users.models import User


class ReactToPostViewTests(TestCase):
    """Постановка/смена/снятие реакции на пост."""

    def setUp(self):
        owner = User.objects.create_user(login="owner", password="testpass123")
        pet = Pet.objects.create(owner=owner, name="Barsik")
        self.post = Post.objects.create(pet=pet, title="Прогулка")
        self.user = User.objects.create_user(login="fan", password="testpass123")
        self.client.login(login="fan", password="testpass123")

    def react(self, reaction_type):
        return self.client.post(
            reverse("reactions:react_post", args=[self.post.pk]), data={"reaction_type": reaction_type}
        )

    def test_no_existing_reaction_creates_reaction(self):
        self.react(Reaction.LIKE)

        actual = Reaction.objects.get(user=self.user, post=self.post).reaction_type
        self.assertEqual(actual, Reaction.LIKE)

    def test_same_reaction_type_removes_reaction(self):
        self.react(Reaction.LIKE)

        self.react(Reaction.LIKE)

        actual = Reaction.objects.filter(user=self.user, post=self.post).exists()
        self.assertFalse(actual)

    def test_different_reaction_type_changes_type(self):
        self.react(Reaction.LIKE)

        self.react(Reaction.HEART)

        actual = Reaction.objects.get(user=self.user, post=self.post).reaction_type
        self.assertEqual(actual, Reaction.HEART)

    def test_changing_type_does_not_create_extra_row(self):
        self.react(Reaction.LIKE)

        self.react(Reaction.HEART)

        actual = Reaction.objects.filter(user=self.user, post=self.post).count()
        self.assertEqual(actual, 1)

    def test_redirects_to_post_detail(self):
        response = self.react(Reaction.LIKE)

        self.assertRedirects(response, reverse("posts:detail", args=[self.post.pk]))

    def test_anonymous_redirects_to_login(self):
        self.client.logout()

        response = self.react(Reaction.LIKE)

        expected = f"{reverse('users:login')}?next={reverse('reactions:react_post', args=[self.post.pk])}"
        self.assertRedirects(response, expected)

    def test_nonexistent_post_returns_404(self):
        response = self.client.post(
            reverse("reactions:react_post", args=[999999]), data={"reaction_type": Reaction.LIKE}
        )

        actual = response.status_code
        self.assertEqual(actual, 404)


class ReactToCommentViewTests(TestCase):
    """Постановка/смена/снятие реакции на комментарий."""

    def setUp(self):
        owner = User.objects.create_user(login="owner", password="testpass123")
        pet = Pet.objects.create(owner=owner, name="Barsik")
        self.post = Post.objects.create(pet=pet, title="Прогулка")
        self.comment = Comment.objects.create(post=self.post, user=owner, description="Милота!")
        self.user = User.objects.create_user(login="fan", password="testpass123")
        self.client.login(login="fan", password="testpass123")

    def react(self, reaction_type):
        return self.client.post(
            reverse("reactions:react_comment", args=[self.comment.pk]), data={"reaction_type": reaction_type}
        )

    def test_no_existing_reaction_creates_reaction(self):
        self.react(Reaction.LIKE)

        actual = Reaction.objects.get(user=self.user, comment=self.comment).reaction_type
        self.assertEqual(actual, Reaction.LIKE)

    def test_same_reaction_type_removes_reaction(self):
        self.react(Reaction.LIKE)

        self.react(Reaction.LIKE)

        actual = Reaction.objects.filter(user=self.user, comment=self.comment).exists()
        self.assertFalse(actual)

    def test_different_reaction_type_changes_type(self):
        self.react(Reaction.LIKE)

        self.react(Reaction.HEART)

        actual = Reaction.objects.get(user=self.user, comment=self.comment).reaction_type
        self.assertEqual(actual, Reaction.HEART)

    def test_redirects_to_comments_post_detail(self):
        response = self.react(Reaction.LIKE)

        self.assertRedirects(response, reverse("posts:detail", args=[self.post.pk]))

    def test_anonymous_redirects_to_login(self):
        self.client.logout()

        response = self.react(Reaction.LIKE)

        expected = f"{reverse('users:login')}?next={reverse('reactions:react_comment', args=[self.comment.pk])}"
        self.assertRedirects(response, expected)

    def test_nonexistent_comment_returns_404(self):
        response = self.client.post(
            reverse("reactions:react_comment", args=[999999]), data={"reaction_type": Reaction.LIKE}
        )

        actual = response.status_code
        self.assertEqual(actual, 404)
