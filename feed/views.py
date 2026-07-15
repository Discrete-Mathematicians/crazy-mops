from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from feed.services import get_pet_rating, get_popular_tags, get_upcoming_birthdays, sort_by_nearest_birthday
from posts.models import Post


class FeedView(LoginRequiredMixin, ListView):
    template_name = "feed/feed.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return (
            Post.objects.filter(pet__subscription__user=self.request.user)
            .select_related("pet__owner")
            .prefetch_related("media", "tags")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pets = get_upcoming_birthdays(self.request.user)
        context["upcoming_birthdays"] = sort_by_nearest_birthday(pets)

        pet_rating = get_pet_rating()
        context["pet_rating"] = pet_rating
        context["pet_of_week"] = pet_rating[0] if pet_rating else None

        context["popular_tags"] = get_popular_tags()
        return context
