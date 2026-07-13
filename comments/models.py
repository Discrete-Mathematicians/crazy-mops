from django.conf import settings
from django.db import models

from posts.models import Post


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="пост",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="автор",
    )
    reply_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True,
        verbose_name="ответ на комментарий",
    )
    description = models.TextField("текст")
    created_at = models.DateTimeField("создан", auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"

    def __str__(self):
        return f"{self.user}: {self.description[:30]}"


class CommentMedia(models.Model):
    IMAGE = "image"
    VIDEO = "video"
    MEDIA_TYPE_CHOICES = [
        (IMAGE, "Изображение"),
        (VIDEO, "Видео"),
    ]

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="media")
    media_url = models.FileField(upload_to="comment_media/")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    display_order = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"Медиа #{self.pk} к комментарию #{self.comment_id}"
