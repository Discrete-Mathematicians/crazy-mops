from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "login",
        "display_name",
        "email",
        "account_type",
        "is_staff",
    )
    search_fields = ("username", "login", "display_name", "email")
    list_filter = ("account_type", "is_staff", "is_active")

    fieldsets = UserAdmin.fieldsets + (
        (
            "Профиль crazy-mops",
            {"fields": ("login", "display_name", "avatar", "account_type")},
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Профиль crazy-mops",
            {"fields": ("login", "display_name", "account_type")},
        ),
    )
