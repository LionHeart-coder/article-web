from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from posts import posts_settings
from posts.forms import CommentForm, PostForm
from posts.models import Post, Like, Group


@login_required
def new_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('index')
    return render(request, 'posts/new_post.html', {'form': form})


@login_required
def delete_post(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if request.user == post.author:
        post.delete()
    return redirect(request.GET.get('next'))


def post_view(request, username, post_id):
    post = get_object_or_404(
        Post.objects.annotate_like(request.user).prefetch_related(
            'comments__author',
            'comments__replies',
            'comments__replies__author',
        ),
        id=post_id,
        author__username=username,
    )
    form = CommentForm()
    return render(request, 'posts/post.html', {'post': post, 'form': form})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if post.author != request.user:
        return redirect('post', username=username, post_id=post_id)

    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )

    if form.is_valid():
        form.save()
        return redirect('post', username=username, post_id=post_id)

    return render(
        request, 'posts/new_post.html', {'form': form, 'edit_post': post}
    )


@login_required
def post_like(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    if Like.objects.filter(user=request.user, post=post).exists():
        Like.objects.filter(user=request.user, post=post).delete()
    else:
        Like.objects.get_or_create(user=request.user, post=post)
    post = get_object_or_404(
        Post.objects.annotate_like(request.user),
        author__username=username,
        id=post_id,
    )
    return JsonResponse(
        {'number_of_likes': post.likes.count(), 'liked': post.liked}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = (
        group.posts.all()
            .select_related('author')
            .prefetch_related('comments')
            .annotate_like(request.user)
    )
    paginator = Paginator(post_list, posts_settings.GROUP_NUMBER_OF_POSTS)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {'group': group, 'page': page, 'paginator': paginator}
    return render(request, 'posts/group.html', context)
