from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from pets.models import Pet
from posts.forms import PostForm
from posts.models import Post


class PostOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Редактировать/удалять пост может владелец питомца или админ."""

    def test_func(self):
        post = self.get_object()
        user = self.request.user
        return user == post.pet.owner or user.is_staff


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"

    def get_pet(self):
        return get_object_or_404(Pet, pk=self.kwargs["pet_pk"])

    def test_func(self):
        # постить можно только от имени своего питомца (или админ)
        user = self.request.user
        return user == self.get_pet().owner or user.is_staff

    def form_valid(self, form):
        form.instance.pet = self.get_pet()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["pet"] = self.get_pet()
        return ctx


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx["can_manage"] = user.is_authenticated and (user == self.object.pet.owner or user.is_staff)
        return ctx


class PostUpdateView(PostOwnerMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"


class PostDeleteView(PostOwnerMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"

    def get_success_url(self):
        return reverse("pets:detail", kwargs={"pk": self.object.pet.pk})
