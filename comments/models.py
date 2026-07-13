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
