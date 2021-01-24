from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_post, name='new_post'),
    path('group/<slug:slug>/', views.group_posts, name='group'),
    path('follow/', views.follow_index, name='follow_index'),
    path('<username>/<int:post_id>/', views.post_view, name='post'),
    path('<username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path(
        '<username>/<int:post_id>/comment/',
        views.add_comment,
        name='add_comment',
    ),
    path(
        '<username>/<int:post_id>/<int:comment_id>/reply/',
        views.add_reply_on_comment,
        name='add_reply',
    ),
    path('<username>/follow/', views.profile_follow, name='profile_follow'),
    path(
        '<username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow',
    ),
    path('post/<username>/<int:post_id>/like/', views.post_like, name='post_like'),
    path('post/<username>/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    # TODO перенести в users
    path('user/<int:user_id>/add_social_link/', views.add_social_link, name='add_social_link'),
    path('post/<int:author_id>/<int:social_link_id>/delete_social_link/', views.delete_social_link, name='delete_social_link'),
    path('<username>/', views.profile, name='profile'),
]
