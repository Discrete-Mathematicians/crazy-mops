from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "reply_comment", "created_at")
    list_filter = ("created_at",)
    search_fields = ("description", "user__login", "post__title")
    autocomplete_fields = ("post", "user", "reply_comment")
    list_select_related = ("post", "user", "reply_comment")
