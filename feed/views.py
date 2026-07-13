from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from feed.services import get_upcoming_birthdays, sort_by_nearest_birthday
from posts.models import Post


class FeedView(LoginRequiredMixin, ListView):
    template_name = "feed/feed.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return (
            Post.objects.filter(pet__subscription__user=self.request.user)
            .select_related("pet")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pets = get_upcoming_birthdays(self.request.user)
        context["upcoming_birthdays"] = sort_by_nearest_birthday(pets)
        return context
