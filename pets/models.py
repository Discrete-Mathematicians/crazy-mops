from datetime import date

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

    @property
    def age_years(self):
        """Возраст в полных годах на сегодня; None, если дата рождения не указана."""
        if not self.birthday:
            return None
        today = date.today()
        years = today.year - self.birthday.year
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            years -= 1
        return years

    @property
    def age_label(self):
        years = self.age_years
        if years is None:
            return ""
        if years % 10 == 1 and years % 100 != 11:
            word = "год"
        elif 2 <= years % 10 <= 4 and not 12 <= years % 100 <= 14:
            word = "года"
        else:
            word = "лет"
        return f"{years} {word}"

    @property
    def sex_icon(self):
        if self.sex == self.Sex.MALE:
            return "♂"
        if self.sex == self.Sex.FEMALE:
            return "♀"
        return ""

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("pets:detail", kwargs={"pk": self.pk})
