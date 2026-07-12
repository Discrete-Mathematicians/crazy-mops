from django.db import models
from django.urls import reverse

from pets.models import Pet


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

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "пост"
        verbose_name_plural = "посты"

    def __str__(self):
        return f"{self.pet.name}: {self.title}"

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"pk": self.pk})
