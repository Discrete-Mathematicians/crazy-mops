from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class AccountType(models.TextChoices):
        USER = "user", "Пользователь"
        ADMIN = "admin", "Администратор"

    login = models.CharField("Логин", max_length=20, unique=True)
    display_name = models.CharField("Отображаемое имя", max_length=150)
    avatar = models.ImageField("Аватар", upload_to="AVATARS/", blank=True, null=True)
    account_type = models.CharField(
        "Тип аккаунта",
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.USER,
    )

    def __str__(self):
        return self.display_name or self.username
