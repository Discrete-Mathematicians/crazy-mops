from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from comments.forms import CommentForm
from pets.models import Pet
from posts.forms import PostForm
from posts.models import Post, PostMedia


class PostOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Редактировать/удалять пост может владелец питомца или админ."""

    def test_func(self):
        post = self.get_object()
        user = self.request.user
        return user == post.pet.owner or user.is_staff


class PostMediaTagsMixin:
    """Сохраняет теги и загруженные медиафайлы после сохранения поста."""

    def save_related(self, form):
        form.save_tags(self.object)

        existing_count = self.object.media.count()
        files = form.cleaned_data.get("media", [])
        for order, uploaded_file in enumerate(files, start=existing_count):
            media_type = (
                PostMedia.MediaType.IMAGE
                if (uploaded_file.content_type or "").startswith("image")
                else PostMedia.MediaType.VIDEO
            )
            PostMedia.objects.create(
                post=self.object,
                media_url=uploaded_file,
                media_type=media_type,
                display_order=order,
            )


class PostCreateView(PostMediaTagsMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
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
        response = super().form_valid(form)
        self.save_related(form)
        return response

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
        ctx["comments"] = self.object.comments.filter(reply_comment__isnull=True).select_related("user")
        ctx["comment_form"] = CommentForm()
        return ctx


class PostUpdateView(PostMediaTagsMixin, PostOwnerMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        self.save_related(form)
        return response


class PostDeleteView(PostOwnerMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"

    def get_success_url(self):
        return reverse("pets:detail", kwargs={"pk": self.object.pet.pk})


class PostsByTagView(ListView):
    model = Post
    template_name = "posts/posts_by_tag.html"
    context_object_name = "posts_page"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs["tag"]).order_by("-created_at")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tag_name"] = self.kwargs["tag"]
        return ctx
