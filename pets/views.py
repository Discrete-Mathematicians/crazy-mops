from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["can_manage"] = user.is_authenticated and self.object.owner_id == user.id
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
