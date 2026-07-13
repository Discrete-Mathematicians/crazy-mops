from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from posts.models import Post

from .forms import CommentForm
from .models import Comment


@login_required
@require_POST
def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
    return redirect("posts:detail", pk=post.pk)


@login_required
@require_POST
def add_reply(request, comment_pk):
    parent = get_object_or_404(Comment, pk=comment_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.post = parent.post
        reply.user = request.user
        reply.reply_comment = parent
        reply.save()
    return redirect("posts:detail", pk=parent.post_id)


@login_required
@require_POST
def delete_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user
    if user != comment.user and not user.is_staff:
        return HttpResponseForbidden()
    post_pk = comment.post_id
    comment.delete()
    return redirect("posts:detail", pk=post_pk)
