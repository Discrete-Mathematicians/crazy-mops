from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.templatetags.static import static

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class AccountType(models.TextChoices):
        USER = "user", "Пользователь"
        ADMIN = "admin", "Администратор"

    login = models.CharField("Логин", max_length=20, unique=True)
    display_name = models.CharField("Отображаемое имя", max_length=150, blank=True)
    first_name = models.CharField("Имя", max_length=150, blank=True)
    last_name = models.CharField("Фамилия", max_length=150, blank=True)
    email = models.EmailField("Email", blank=True)
    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True)
    account_type = models.CharField(
        "Тип аккаунта",
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.USER,
    )

    is_staff = models.BooleanField("Статус персонала", default=False)
    is_active = models.BooleanField("Активен", default=True)
    date_joined = models.DateTimeField("Дата регистрации", auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = []  # login и password спрашиваются всегда

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    @property
    def avatar_url(self):
        """URL аватара пользователя или дефолтной картинки из статики."""
        if self.avatar:
            return self.avatar.url
        return static("users/img/default_avatar.png")

    def save(self, *args, **kwargs):
        # display_name = login, пока пользователь не задал своё
        if not self.display_name:
            self.display_name = self.login
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Имя и фамилия через пробел; пустая строка, если оба не заполнены."""
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.display_name or self.login
