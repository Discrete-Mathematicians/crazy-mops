from django.test import TestCase
from django.urls import reverse

from pets.models import Pet
from posts.models import Post
from users.models import User


class PostCreateViewTests(TestCase):
    """Создание поста через posts:create."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")
        self.other_user = User.objects.create_user(login="other", password="testpass123")
        self.admin = User.objects.create_user(login="admin", password="testpass123", is_staff=True)
        self.pet = Pet.objects.create(owner=self.owner, name="Barsik")

    def test_get_form_returns_200_for_pet_owner(self):
        self.client.login(login="owner", password="testpass123")

        response = self.client.get(reverse("posts:create", args=[self.pet.pk]))

        actual = response.status_code
        self.assertEqual(actual, 200)

    def test_get_form_returns_200_for_admin(self):
        self.client.login(login="admin", password="testpass123")

        response = self.client.get(reverse("posts:create", args=[self.pet.pk]))

        actual = response.status_code
        self.assertEqual(actual, 200)

    def test_other_user_gets_403(self):
        self.client.login(login="other", password="testpass123")

        response = self.client.get(reverse("posts:create", args=[self.pet.pk]))

        actual = response.status_code
        self.assertEqual(actual, 403)

    def test_anonymous_redirects_to_login(self):
        response = self.client.get(reverse("posts:create", args=[self.pet.pk]))

        expected = f"{reverse('users:login')}?next={reverse('posts:create', args=[self.pet.pk])}"
        self.assertRedirects(response, expected)

    def test_nonexistent_pet_returns_404(self):
        self.client.login(login="owner", password="testpass123")

        response = self.client.get(reverse("posts:create", args=[999999]))

        actual = response.status_code
        self.assertEqual(actual, 404)

    def test_post_valid_data_creates_post(self):
        self.client.login(login="owner", password="testpass123")

        self.client.post(reverse("posts:create", args=[self.pet.pk]), data={"title": "Прогулка", "description": ""})

        actual = Post.objects.filter(title="Прогулка", pet=self.pet).exists()
        self.assertTrue(actual)

    def test_post_valid_data_redirects_to_detail(self):
        self.client.login(login="owner", password="testpass123")

        response = self.client.post(
            reverse("posts:create", args=[self.pet.pk]), data={"title": "Прогулка", "description": ""}
        )

        post = Post.objects.get(title="Прогулка")
        self.assertRedirects(response, reverse("posts:detail", args=[post.pk]))


class PostDetailViewTests(TestCase):
    """Просмотр поста через posts:detail."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")
        self.pet = Pet.objects.create(owner=self.owner, name="Barsik")
        self.post = Post.objects.create(pet=self.pet, title="Прогулка")

    def get_can_manage(self):
        response = self.client.get(reverse("posts:detail", args=[self.post.pk]))
        return response.context["can_manage"]

    def test_guest_gets_200(self):
        response = self.client.get(reverse("posts:detail", args=[self.post.pk]))

        actual = response.status_code
        self.assertEqual(actual, 200)

    def test_can_manage_true_for_owner(self):
        self.client.login(login="owner", password="testpass123")

        actual = self.get_can_manage()

        self.assertTrue(actual)

    def test_can_manage_true_for_admin(self):
        User.objects.create_user(login="admin", password="testpass123", is_staff=True)
        self.client.login(login="admin", password="testpass123")

        actual = self.get_can_manage()

        self.assertTrue(actual)

    def test_can_manage_false_for_other_user(self):
        User.objects.create_user(login="other", password="testpass123")
        self.client.login(login="other", password="testpass123")

        actual = self.get_can_manage()

        self.assertFalse(actual)

    def test_can_manage_false_for_anonymous(self):
        actual = self.get_can_manage()

        self.assertFalse(actual)

    def test_nonexistent_post_returns_404(self):
        response = self.client.get(reverse("posts:detail", args=[999999]))

        actual = response.status_code
        self.assertEqual(actual, 404)


class PostUpdateViewTests(TestCase):
    """Редактирование поста через posts:edit."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")
        self.other_user = User.objects.create_user(login="other", password="testpass123")
        self.pet = Pet.objects.create(owner=self.owner, name="Barsik")
        self.post = Post.objects.create(pet=self.pet, title="Прогулка")

    def test_get_form_returns_200_for_owner(self):
        self.client.login(login="owner", password="testpass123")

        response = self.client.get(reverse("posts:edit", args=[self.post.pk]))

        actual = response.status_code
        self.assertEqual(actual, 200)

    def test_post_valid_data_updates_title(self):
        self.client.login(login="owner", password="testpass123")

        self.client.post(
            reverse("posts:edit", args=[self.post.pk]), data={"title": "Новый заголовок", "description": ""}
        )

        actual = Post.objects.get(pk=self.post.pk).title
        self.assertEqual(actual, "Новый заголовок")

    def test_post_valid_data_redirects_to_detail(self):
        self.client.login(login="owner", password="testpass123")

        response = self.client.post(
            reverse("posts:edit", args=[self.post.pk]), data={"title": "Новый заголовок", "description": ""}
        )

        self.assertRedirects(response, reverse("posts:detail", args=[self.post.pk]))

    def test_other_user_gets_403(self):
        self.client.login(login="other", password="testpass123")

        response = self.client.get(reverse("posts:edit", args=[self.post.pk]))

        actual = response.status_code
        self.assertEqual(actual, 403)

    def test_anonymous_redirects_to_login(self):
        response = self.client.get(reverse("posts:edit", args=[self.post.pk]))

        expected = f"{reverse('users:login')}?next={reverse('posts:edit', args=[self.post.pk])}"
        self.assertRedirects(response, expected)

    def test_admin_can_edit_foreign_post(self):
        User.objects.create_user(login="admin", password="testpass123", is_staff=True)
        self.client.login(login="admin", password="testpass123")

        response = self.client.get(reverse("posts:edit", args=[self.post.pk]))

        actual = response.status_code
        self.assertEqual(actual, 200)


class PostDeleteViewTests(TestCase):
    """Удаление поста через posts:delete."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")
        self.other_user = User.objects.create_user(login="other", password="testpass123")
        self.pet = Pet.objects.create(owner=self.owner, name="Barsik")
        self.post = Post.objects.create(pet=self.pet, title="Прогулка")

    def test_owner_can_delete_post(self):
        self.client.login(login="owner", password="testpass123")

        self.client.post(reverse("posts:delete", args=[self.post.pk]))

        actual = Post.objects.filter(pk=self.post.pk).exists()
        self.assertFalse(actual)

    def test_delete_redirects_to_pet_detail(self):
        self.client.login(login="owner", password="testpass123")

        response = self.client.post(reverse("posts:delete", args=[self.post.pk]))

        self.assertRedirects(response, reverse("pets:detail", args=[self.pet.pk]))

    def test_other_user_gets_403(self):
        self.client.login(login="other", password="testpass123")

        response = self.client.post(reverse("posts:delete", args=[self.post.pk]))

        actual = response.status_code
        self.assertEqual(actual, 403)

    def test_anonymous_redirects_to_login(self):
        response = self.client.get(reverse("posts:delete", args=[self.post.pk]))

        expected = f"{reverse('users:login')}?next={reverse('posts:delete', args=[self.post.pk])}"
        self.assertRedirects(response, expected)

    def test_admin_can_delete_foreign_post(self):
        User.objects.create_user(login="admin", password="testpass123", is_staff=True)
        self.client.login(login="admin", password="testpass123")

        self.client.post(reverse("posts:delete", args=[self.post.pk]))

        actual = Post.objects.filter(pk=self.post.pk).exists()
        self.assertFalse(actual)


class PostsByTagViewTests(TestCase):
    """Список постов по тегу через posts:by_tag."""

    def setUp(self):
        owner = User.objects.create_user(login="owner", password="testpass123")
        pet = Pet.objects.create(owner=owner, name="Barsik")
        self.matching_post = Post.objects.create(pet=pet, title="Прогулка")
        self.matching_post.tags.create(name="парк")
        other_post = Post.objects.create(pet=pet, title="Дома")
        other_post.tags.create(name="дом")

    def test_guest_gets_200(self):
        response = self.client.get(reverse("posts:by_tag", args=["парк"]))

        actual = response.status_code
        self.assertEqual(actual, 200)

    def test_filters_by_exact_tag_name(self):
        response = self.client.get(reverse("posts:by_tag", args=["парк"]))

        actual = list(response.context["posts_page"])
        self.assertEqual(actual, [self.matching_post])

    def test_nonexistent_tag_returns_200(self):
        response = self.client.get(reverse("posts:by_tag", args=["несуществующий"]))

        actual = response.status_code
        self.assertEqual(actual, 200)

    def test_nonexistent_tag_returns_empty_list(self):
        response = self.client.get(reverse("posts:by_tag", args=["несуществующий"]))

        actual = list(response.context["posts_page"])
        self.assertEqual(actual, [])
