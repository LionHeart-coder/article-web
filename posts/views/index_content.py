from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, render_to_response

from posts import posts_settings
from posts.models import Post, User


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


def best_articles(request):
    post_list = (
        Post.objects.annotate(rating=Count('likes') + Count('comments'))
        .order_by('-rating')[:5]
        .select_related('group', 'author')
        .prefetch_related('comments', 'likes')
        .annotate_like(request.user)
    )

    paginator = Paginator(post_list, posts_settings.INDEX_NUMBER_OF_POSTS)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
        'request': request,
    }
    return render_to_response('posts/includes/index_content.html', context)


def best_authors(request):
    author_list = User.objects.annotate(
        rating=Count('posts__comments', distinct=True)
        + Count('posts__likes', distinct=True)
        + Count('following')
    ).order_by('-rating')[:6]
    context = {'author_list': author_list}
    return render_to_response('posts/includes/best_authors.html', context)


@login_required
def favorites_authors(request, username):
    user = get_object_or_404(User, username=username)
    if request.user == user:
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
        return render_to_response('posts/includes/index_content.html', context)
    return HttpResponseBadRequest()
