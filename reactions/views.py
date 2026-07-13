from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from comments.models import Comment
from posts.models import Post

from .models import Reaction


@login_required
@require_POST
def react_to_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    reaction_type = int(request.POST["reaction_type"])
    _toggle_reaction(request.user, reaction_type, post=post)
    return redirect("posts:detail", pk=post.pk)


@login_required
@require_POST
def react_to_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    reaction_type = int(request.POST["reaction_type"])
    _toggle_reaction(request.user, reaction_type, comment=comment)
    return redirect("posts:detail", pk=comment.post_id)


def _toggle_reaction(user, reaction_type, post=None, comment=None):
    existing = Reaction.objects.filter(user=user, post=post, comment=comment).first()
    if existing is None:
        Reaction.objects.create(user=user, post=post, comment=comment, reaction_type=reaction_type)
    elif existing.reaction_type == reaction_type:
        existing.delete()
    else:
        existing.reaction_type = reaction_type
        existing.save(update_fields=["reaction_type"])
