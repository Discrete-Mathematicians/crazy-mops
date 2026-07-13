from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from posts.models import Post

from .forms import CommentForm
from .models import Comment, CommentMedia


@login_required
@require_POST
def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST, request.FILES)
    print('FILES:', request.FILES)
    print('is_valid:', form.is_valid())
    print('errors:', form.errors)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        _save_comment_media(comment, request.FILES.getlist('media'))
    return redirect('posts:detail', pk=post.pk)


@login_required
@require_POST
def add_reply(request, comment_pk):
    parent = get_object_or_404(Comment, pk=comment_pk)
    form = CommentForm(request.POST, request.FILES)
    print('FILES:', request.FILES)          # временно
    print('is_valid:', form.is_valid())      # временно
    print('errors:', form.errors)            # временно
    if form.is_valid():
        reply = form.save(commit=False)
        reply.post = parent.post
        reply.user = request.user
        reply.reply_comment = parent
        reply.save()
        _save_comment_media(reply, request.FILES.getlist('media'))
    return redirect('posts:detail', pk=parent.post_id)


@login_required
@require_POST
def delete_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user
    if user != comment.user and not user.is_staff:
        return HttpResponseForbidden()
    post_pk = comment.post_id
    comment.delete()
    return redirect('posts:detail', pk=post_pk)


def _save_comment_media(comment, files):
    for order, file in enumerate(files):
        media_type = CommentMedia.IMAGE if file.content_type.startswith('image/') else CommentMedia.VIDEO
        CommentMedia.objects.create(
            comment=comment,
            media_url=file,
            media_type=media_type,
            display_order=order,
        )