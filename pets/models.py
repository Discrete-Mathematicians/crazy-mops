from django.conf import settings
from django.db import models
from django.urls import reverse


class Pet(models.Model):
    """Карточка питомца. Поля соответствуют схеме `pet` из docs/MODELS.md."""

    class PetType(models.TextChoices):
        DOG = "dog", "Собака"
        CAT = "cat", "Кошка"
        BIRD = "bird", "Птица"
        RODENT = "rodent", "Грызун"
        REPTILE = "reptile", "Рептилия"
        OTHER = "other", "Другое"

    class Sex(models.IntegerChoices):
        MALE = 0, "Мальчик"
        FEMALE = 1, "Девочка"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pets",
        verbose_name="Владелец",
    )
    name = models.CharField("Кличка", max_length=255)
    avatar = models.ImageField("Аватар", upload_to="pets/avatars/", blank=True, null=True)
    breed = models.CharField("Порода", max_length=100, blank=True)
    birthday = models.DateField("Дата рождения", blank=True, null=True)
    eye_color = models.CharField("Цвет глаз", max_length=50, blank=True)
    coat_color = models.CharField("Окрас", max_length=50, blank=True)
    pet_type = models.CharField("Вид", max_length=50, choices=PetType.choices, default=PetType.OTHER)
    sex = models.SmallIntegerField("Пол", choices=Sex.choices, blank=True, null=True)

    class Meta:
        verbose_name = "Питомец"
        verbose_name_plural = "Питомцы"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("pets:detail", kwargs={"pk": self.pk})
