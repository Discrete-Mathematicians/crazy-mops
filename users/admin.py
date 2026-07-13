from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ("login",)
    list_display = (
        "login",
        "display_name",
        "email",
        "account_type",
        "is_staff",
    )
    search_fields = ("login", "display_name", "email")
    list_filter = ("account_type", "is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("login", "password")}),
        (
            "Профиль",
            {"fields": ("display_name", "first_name", "last_name", "email", "avatar", "account_type")},
        ),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = ("date_joined", "last_login")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("login", "password1", "password2"),
            },
        ),
    )
