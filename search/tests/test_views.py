from django.test import TestCase
from django.urls import reverse

from pets.models import Pet
from users.models import User


class OwnersSearchTests(TestCase):
    """Поиск по владельцам (display_name)."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123", display_name="Мурзик Иванов")

    def search(self, q, search_type="owners"):
        return self.client.get(reverse("search:search"), {"q": q, "type": search_type})

    def test_finds_by_display_name_substring(self):
        response = self.search("урз")

        actual = list(response.context["results"])
        self.assertEqual(actual, [self.owner])

    def test_is_case_insensitive(self):
        response = self.search("МУРЗ")

        actual = list(response.context["results"])
        self.assertEqual(actual, [self.owner])

    def test_no_results_returns_empty_list(self):
        response = self.search("zzznonexistent")

        actual = list(response.context["results"])
        self.assertEqual(actual, [])

    def test_no_results_returns_200(self):
        response = self.search("zzznonexistent")

        actual = response.status_code
        self.assertEqual(actual, 200)


class PetsSearchTests(TestCase):
    """Поиск по питомцам (name)."""

    def setUp(self):
        owner = User.objects.create_user(login="owner", password="testpass123")
        self.pet = Pet.objects.create(owner=owner, name="Барсик")

    def search(self, q, search_type="pets"):
        return self.client.get(reverse("search:search"), {"q": q, "type": search_type})

    def test_finds_by_name_substring(self):
        response = self.search("арс")

        actual = list(response.context["results"])
        self.assertEqual(actual, [self.pet])

    def test_is_case_insensitive(self):
        response = self.search("АРС")

        actual = list(response.context["results"])
        self.assertEqual(actual, [self.pet])


class SearchPageAccessTests(TestCase):
    """Доступность страницы поиска."""

    def test_accessible_to_guest_without_query(self):
        response = self.client.get(reverse("search:search"))

        actual = response.status_code
        self.assertEqual(actual, 200)

    def test_accessible_to_guest_with_query(self):
        response = self.client.get(reverse("search:search"), {"q": "test", "type": "owners"})

        actual = response.status_code
        self.assertEqual(actual, 200)


class SearchPaginationTests(TestCase):
    """Пагинация результатов поиска."""

    def setUp(self):
        for i in range(9):
            User.objects.create_user(login=f"owner{i}", password="testpass123", display_name=f"Мурзик {i}")

    def search_page(self, page=None):
        params = {"q": "Мурзик", "type": "owners"}
        if page is not None:
            params["page"] = page
        return self.client.get(reverse("search:search"), params)

    def test_first_page_has_eight_results(self):
        response = self.search_page()

        actual = len(response.context["results"])
        self.assertEqual(actual, 8)

    def test_first_page_is_paginated(self):
        response = self.search_page()

        actual = response.context["is_paginated"]
        self.assertTrue(actual)

    def test_second_page_has_remaining_result(self):
        response = self.search_page(page=2)

        actual = len(response.context["results"])
        self.assertEqual(actual, 1)
