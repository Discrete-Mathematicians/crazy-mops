from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from posts.models import Post


class FeedView(LoginRequiredMixin, ListView):
    template_name = 'feed/feed.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return (
            Post.objects
            .filter(pet__subscription__user=self.request.user)
            .select_related('pet')
            .order_by('-created_at')
        )