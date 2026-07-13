from django.contrib import admin

from .models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "pet_type", "breed", "owner", "birthday", "sex")
    list_filter = ("pet_type", "sex")
    search_fields = ("name", "breed", "owner__login")
    autocomplete_fields = ("owner",)
    list_select_related = ("owner",)
