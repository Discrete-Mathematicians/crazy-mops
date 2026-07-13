from datetime import date
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from feed.services import get_upcoming_birthdays, sort_by_nearest_birthday
from pets.models import Pet
from subscriptions.models import Subscription
from users.models import User


def patched_today(mock_date, year, month, day):
    mock_date.today.return_value = date(year, month, day)
    mock_date.side_effect = lambda *args, **kwargs: date(*args, **kwargs)


class GetUpcomingBirthdaysTests(TestCase):
    """Питомцы для календаря дней рождения: только подписки, с заполненным birthday."""

    def setUp(self):
        self.viewer = User.objects.create_user(login="viewer", password="testpass123")
        self.owner = User.objects.create_user(login="owner", password="testpass123")

    def test_includes_subscribed_pet_with_birthday(self):
        pet = Pet.objects.create(owner=self.owner, name="Barsik", birthday=date(2020, 5, 1))
        Subscription.objects.create(user=self.viewer, pet=pet)

        actual = list(get_upcoming_birthdays(self.viewer))

        self.assertEqual(actual, [pet])

    def test_excludes_pet_without_birthday(self):
        pet = Pet.objects.create(owner=self.owner, name="Barsik")
        Subscription.objects.create(user=self.viewer, pet=pet)

        actual = list(get_upcoming_birthdays(self.viewer))

        self.assertEqual(actual, [])

    def test_excludes_pet_user_is_not_subscribed_to(self):
        Pet.objects.create(owner=self.owner, name="Barsik", birthday=date(2020, 5, 1))

        actual = list(get_upcoming_birthdays(self.viewer))

        self.assertEqual(actual, [])


class SortByNearestBirthdayTests(TestCase):
    """Сортировка питомцев по дате ближайшего дня рождения (месяц/день, без года)."""

    def setUp(self):
        self.owner = User.objects.create_user(login="owner", password="testpass123")

    def make_pet(self, name, month, day):
        return Pet.objects.create(owner=self.owner, name=name, birthday=date(2000, month, day))

    @patch("feed.services.date")
    def test_sorts_by_nearest_upcoming_date_within_same_year(self, mock_date):
        patched_today(mock_date, 2026, 1, 5)
        near = self.make_pet("Near", 1, 10)
        far = self.make_pet("Far", 2, 1)

        actual = sort_by_nearest_birthday([far, near])

        self.assertEqual(actual, [near, far])

    @patch("feed.services.date")
    def test_wraps_around_year_boundary(self, mock_date):
        patched_today(mock_date, 2026, 12, 30)
        just_passed = self.make_pet("JustPassed", 12, 25)
        just_ahead = self.make_pet("JustAhead", 1, 2)

        actual = sort_by_nearest_birthday([just_passed, just_ahead])

        self.assertEqual(actual, [just_ahead, just_passed])

    @patch("feed.services.date")
    def test_leap_day_birthday_in_non_leap_year_treated_as_march_first(self, mock_date):
        patched_today(mock_date, 2026, 2, 25)
        leap_day_pet = self.make_pet("LeapDay", 2, 29)

        actual = sort_by_nearest_birthday([leap_day_pet])

        self.assertEqual(actual, [leap_day_pet])

    def test_empty_list_stays_empty(self):
        actual = sort_by_nearest_birthday([])

        self.assertEqual(actual, [])


class BirthdayWidgetRenderingTests(TestCase):
    """Виджет дней рождения на странице ленты."""

    def setUp(self):
        self.viewer = User.objects.create_user(login="viewer", password="testpass123")
        self.client.login(login="viewer", password="testpass123")

    def test_empty_widget_shows_placeholder_text(self):
        response = self.client.get(reverse("feed:home"))

        self.assertContains(response, "Подпишитесь на питомцев, чтобы видеть их дни рождения")
