from django import template

from core.permissions import can_manage_object

register = template.Library()


@register.inclusion_tag("includes/comment_item.html")
def comment_item(comment, user):
    """Комментарий с вложенными ответами (рекурсивно). can_delete - по автору комментария, не по владельцу поста."""
    return {
        "comment": comment,
        "user": user,
        "can_delete": can_manage_object(user, comment.user),
        "replies": comment.replies.all(),
    }
