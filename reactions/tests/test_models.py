from django.db import IntegrityError, transaction
from django.test import TestCase

from comments.models import Comment
from pets.models import Pet
from posts.models import Post
from reactions.models import Reaction
from users.models import User


class ReactionUniqueConstraintTests(TestCase):
    """Уникальность реакции: (user+post), (user+comment)."""

    def setUp(self):
        owner = User.objects.create_user(login="owner", password="testpass123")
        pet = Pet.objects.create(owner=owner, name="Barsik")
        self.post = Post.objects.create(pet=pet, title="Прогулка")
        self.comment = Comment.objects.create(post=self.post, user=owner, description="Милота!")
        self.user = User.objects.create_user(login="fan", password="testpass123")

    def test_duplicate_user_post_reaction_raises_integrity_error(self):
        Reaction.objects.create(user=self.user, post=self.post, reaction_type=Reaction.LIKE)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Reaction.objects.create(user=self.user, post=self.post, reaction_type=Reaction.HEART)

    def test_duplicate_user_comment_reaction_raises_integrity_error(self):
        Reaction.objects.create(user=self.user, comment=self.comment, reaction_type=Reaction.LIKE)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Reaction.objects.create(user=self.user, comment=self.comment, reaction_type=Reaction.HEART)

    def test_same_user_can_react_to_post_and_comment_independently(self):
        Reaction.objects.create(user=self.user, post=self.post, reaction_type=Reaction.LIKE)

        Reaction.objects.create(user=self.user, comment=self.comment, reaction_type=Reaction.LIKE)

        actual = Reaction.objects.filter(user=self.user).count()
        self.assertEqual(actual, 2)

    def test_different_users_can_react_to_same_post(self):
        other_user = User.objects.create_user(login="fan2", password="testpass123")
        Reaction.objects.create(user=self.user, post=self.post, reaction_type=Reaction.LIKE)

        Reaction.objects.create(user=other_user, post=self.post, reaction_type=Reaction.LIKE)

        actual = Reaction.objects.filter(post=self.post).count()
        self.assertEqual(actual, 2)


class ReactionExactlyOneTargetConstraintTests(TestCase):
    """Реакция должна ссылаться ровно на один объект: пост или комментарий."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")
        pet = Pet.objects.create(owner=self.owner, name="Barsik")
        self.post = Post.objects.create(pet=pet, title="Прогулка")
        self.user = User.objects.create_user(login="fan", password="testpass123")

    def test_reaction_without_post_or_comment_raises_integrity_error(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Reaction.objects.create(user=self.user, reaction_type=Reaction.LIKE)

    def test_reaction_with_both_post_and_comment_raises_integrity_error(self):
        comment = Comment.objects.create(post=self.post, user=self.owner, description="Милота!")

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Reaction.objects.create(user=self.user, post=self.post, comment=comment, reaction_type=Reaction.LIKE)
