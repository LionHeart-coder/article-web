from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from posts import posts_settings
from posts.forms import SocialLinkForm
from posts.models import Follow, User, SocialLink


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


@login_required
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


@login_required
def delete_social_link(request, author_id, social_link_id):
    author = get_object_or_404(User, id=author_id)
    if request.user == author:
        SocialLink.objects.filter(id=social_link_id).delete()
    return redirect('profile', username=author.username)


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
