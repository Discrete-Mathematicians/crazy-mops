from django.db import models
from django.urls import reverse

from pets.models import Pet


class Tag(models.Model):
    name = models.CharField("название", max_length=50, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name


class Post(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="питомец",
    )
    title = models.CharField("заголовок", max_length=255)
    description = models.TextField("текст", blank=True)
    created_at = models.DateTimeField("создан", auto_now_add=True)
    tags = models.ManyToManyField(
        Tag,
        through="PostTag",
        related_name="posts",
        blank=True,
        verbose_name="теги",
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "пост"
        verbose_name_plural = "посты"

    def __str__(self):
        return f"{self.pet.name}: {self.title}"

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_tags", verbose_name="пост")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="post_tags", verbose_name="тег")

    class Meta:
        unique_together = ("post", "tag")
        verbose_name = "тег поста"
        verbose_name_plural = "теги постов"

    def __str__(self):
        return f"{self.post_id} - {self.tag.name}"


class PostMedia(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", "изображение"
        VIDEO = "video", "видео"

    @property
    def is_video(self):
        return self.media_type == PostMedia.MediaType.VIDEO

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media", verbose_name="пост")
    media_url = models.FileField("файл", upload_to="posts/media/")
    media_type = models.CharField(
        "тип",
        max_length=10,
        choices=MediaType.choices,
        default=MediaType.IMAGE,
    )
    display_order = models.PositiveIntegerField("порядок", default=0)

    class Meta:
        ordering = ("display_order", "id")
        verbose_name = "медиафайл поста"
        verbose_name_plural = "медиафайлы поста"

    def __str__(self):
        return f"{self.post_id}: {self.media_url.name}"
