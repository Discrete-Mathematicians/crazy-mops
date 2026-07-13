from django.conf import settings
from django.db import models

from comments.models import Comment
from posts.models import Post


class Reaction(models.Model):
    LIKE = 0
    HEART = 1
    LAUGH = 2
    WOW = 3
    REACTION_CHOICES = [
        (LIKE, 'лайк'),
        (HEART, 'сердце'),
        (LAUGH, 'смех'),
        (WOW, 'вау'),
    ]
    REACTION_EMOJI = {
        LIKE: '👍',
        HEART: '❤️',
        LAUGH: '😂',
        WOW: '😮',
    }

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="reactions",
        null=True,
        blank=True,
        verbose_name="пост",
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="reactions",
        null=True,
        blank=True,
        verbose_name="комментарий",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reactions",
        verbose_name="автор",
    )
    reaction_type = models.SmallIntegerField('тип реакции', choices=REACTION_CHOICES)
    created_at = models.DateTimeField("создана", auto_now_add=True)

    class Meta:
        verbose_name = "реакция"
        verbose_name_plural = "реакции"
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(post__isnull=False, comment__isnull=True)
                    | models.Q(post__isnull=True, comment__isnull=False)
                ),
                name="reaction_exactly_one_target",
            ),
            models.UniqueConstraint(
                fields=["post", "user"],
                condition=models.Q(post__isnull=False),
                name="reaction_unique_post_user",
            ),
            models.UniqueConstraint(
                fields=["user", "comment"],
                condition=models.Q(comment__isnull=False),
                name="reaction_unique_user_comment",
            ),
        ]

    def __str__(self):
        target = f"пост #{self.post_id}" if self.post_id else f"комментарий #{self.comment_id}"
        return f"{self.user}: {self.get_reaction_type_display()} на {target}"
