from django.contrib import admin

from posts.models import Post, PostMedia, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "pet", "created_at")
    search_fields = ("title", "description")
    list_filter = ("created_at",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display = ("post", "media_type", "display_order")
    list_filter = ("media_type",)
