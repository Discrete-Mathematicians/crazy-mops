from django.contrib import admin

from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "pet", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__login", "pet__name")
    autocomplete_fields = ("user", "pet")
    list_select_related = ("user", "pet")
