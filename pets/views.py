from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import PetForm
from .models import Pet


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().owner_id == self.request.user.id


class PetDetailView(DetailView):
    model = Pet
    template_name = "pets/pet_detail.html"
    context_object_name = "pet"
    posts_per_page = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["can_manage"] = user.is_authenticated and (user == self.object.owner or user.is_staff)

        paginator = Paginator(self.object.posts.all(), self.posts_per_page)
        context["posts_page"] = paginator.get_page(self.request.GET.get("page"))
        return context


class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetForm
    template_name = "pets/pet_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PetUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Pet
    form_class = PetForm
    template_name = "pets/pet_form.html"


class PetDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Pet
    template_name = "pets/pet_confirm_delete.html"
    context_object_name = "pet"
    success_url = reverse_lazy("pets:create")
