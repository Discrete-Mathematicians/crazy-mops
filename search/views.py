from django.contrib.auth import get_user_model
from django.views.generic import ListView

from pets.models import Pet

User = get_user_model()


class SearchView(ListView):
    template_name = "search/search.html"
    context_object_name = "results"
    paginate_by = 8

    def get_search_type(self):
        raw = self.request.GET.get("type", "owners").lower()
        return raw if raw in ("owners", "pets") else "owners"

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        if not q:
            return User.objects.none()
        if self.get_search_type() == "pets":
            return Pet.objects.filter(name__icontains=q)
        return User.objects.filter(display_name__icontains=q)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        ctx["search_type"] = self.get_search_type()
        ctx["searched"] = "q" in self.request.GET

        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["query_string"] = params.urlencode()
        return ctx
