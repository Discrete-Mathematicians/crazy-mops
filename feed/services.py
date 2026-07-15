from datetime import date, timedelta

from django.db.models import Count, F, Q
from django.utils import timezone

from pets.models import Pet
from posts.models import Tag

RATING_WINDOW_DAYS = 7
RATING_TOP_N = 10

POPULAR_TAGS_TOP_N = 6


def get_pet_rating():
    week_ago = timezone.now() - timedelta(days=RATING_WINDOW_DAYS)
    return (
        Pet.objects.select_related("owner")
        .annotate(
            reaction_count=Count(
                "posts__reactions",
                filter=Q(posts__reactions__created_at__gte=week_ago),
                distinct=True,
            ),
            comment_count=Count(
                "posts__comments",
                filter=Q(posts__comments__created_at__gte=week_ago),
                distinct=True,
            ),
        )
        .annotate(rating=F("reaction_count") + F("comment_count"))
        .filter(rating__gt=0)
        .order_by("-rating")[:RATING_TOP_N]
    )


def get_upcoming_birthdays(user):
    return Pet.objects.filter(subscription__user=user).exclude(birthday__isnull=True)


def sort_by_nearest_birthday(pets):
    def days_until(pet):
        today = date.today()
        try:
            next_bday = pet.birthday.replace(year=today.year)
        except ValueError:
            # 29 февраля в невисокосном году - считаем как 1 марта
            next_bday = date(today.year, 3, 1)
        if next_bday < today:
            try:
                next_bday = next_bday.replace(year=today.year + 1)
            except ValueError:
                next_bday = date(today.year + 1, 3, 1)
        return (next_bday - today).days

    return sorted(pets, key=days_until)


def get_popular_tags():
    """Топ тегов по числу постов за все время"""
    return (
        Tag.objects.annotate(post_count=Count("posts", distinct=True))
        .filter(post_count__gt=0)
        .order_by("-post_count")[:POPULAR_TAGS_TOP_N]
    )
