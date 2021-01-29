from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from . import posts_settings
from .forms import CommentForm, PostForm, SocialLinkForm
from .models import Follow, Group, Post, User, Like, Comment, SocialLink


def index(request):
    post_list = (
        Post.objects.all()
        .select_related('group', 'author')
        .prefetch_related('comments', 'likes')
        .annotate_like(request.user)
    )

    paginator = Paginator(post_list, posts_settings.INDEX_NUMBER_OF_POSTS)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'posts/index.html', {'page': page, 'paginator': paginator}
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


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = (
        author.posts.all()
        .select_related('author', 'group')
        .prefetch_related('comments', 'likes')
        .annotate_like(request.user)
    )

    paginator = Paginator(post_list, posts_settings.PROFILE_NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    is_following = (
        request.user.is_authenticated
        and Follow.objects.filter(user=request.user, author=author).exists()
    )
    context = {
        'author': author,
        'is_following': is_following,
        'social_link_form': SocialLinkForm(),
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'posts/profile.html', context)


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


@login_required
def follow_index(request):
    posts_list = (
        Post.objects.filter(author__following__user=request.user)
        .select_related('group', 'author')
        .prefetch_related('comments')
        .annotate_like(request.user)
    )

    paginator = Paginator(
        posts_list, posts_settings.FOLLOW_INDEX_NUMBER_OF_POSTS
    )
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)

    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('profile', username=username)


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


def add_social_link(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = SocialLinkForm(request.POST or None)
    if request.user == user and form.is_valid():
        if form.is_unique(user):
            form.instance.user = user
            form.save()
            return render(
                request,
                'posts/includes/social_link_list.html',
                {'author': user},
            )
    return JsonResponse(form.errors, status=400)


def delete_social_link(request, author_id, social_link_id):
    author = get_object_or_404(User, id=author_id)
    if request.user == author:
        SocialLink.objects.filter(id=social_link_id).delete()
    return redirect('profile', username=author.username)


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)
