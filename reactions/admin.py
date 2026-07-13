from django.contrib import admin

from .models import Reaction


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'reaction_type', 'post', 'comment', 'created_at')
    list_filter = ('reaction_type', 'created_at')
