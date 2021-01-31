from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import CommentForm
from posts.models import Post, Comment


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        form.instance.author = request.user
        form.instance.post = post
        form.save()
    return redirect('post', username=username, post_id=post_id)


@login_required
def add_reply_on_comment(request, username, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    comment = get_object_or_404(Comment, id=comment_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        form.instance.post = post
        form.instance.author = request.user
        form.instance.reply = comment
        form.save()
    return render(
        request, 'posts/comments.html', {'post': post, 'form': CommentForm}
    )
