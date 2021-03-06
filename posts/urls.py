from django.urls import path

from .views import comments_view, index_content, posts_view, profile_view

urlpatterns = [
    path('',
         index_content.index,
         name='index'
         ),
    path('new/',
         posts_view.new_post,
         name='new_post'
         ),
    path('group/<slug:slug>/',
         posts_view.group_posts,
         name='group'
         ),
    path('<username>/<int:post_id>/',
         posts_view.post_view,
         name='post'
         ),
    path('<username>/<int:post_id>/edit/',
         posts_view.post_edit,
         name='post_edit'
         ),

    path('<username>/follow/',
         profile_view.profile_follow,
         name='profile_follow'
         ),
    path(
        '<username>/unfollow/',
        profile_view.profile_unfollow,
        name='profile_unfollow',
    ),
    path('post/<username>/<int:post_id>/like/',
         posts_view.post_like,
         name='post_like'
         ),
    path('post/<username>/<int:post_id>/delete/',
         posts_view.delete_post,
         name='delete_post'
         ),
    path(
        '<username>/<int:post_id>/comment/',
        comments_view.add_comment,
        name='add_comment',
    ),
    path(
        '<username>/<int:post_id>/<int:comment_id>/reply/',
        comments_view.add_reply_on_comment,
        name='add_reply',
    ),
    # ajax links
    path('user/<int:user_id>/add_social_link/',
         profile_view.add_social_link,
         name='add_social_link'
         ),
    path('post/<int:author_id>/<int:social_link_id>/delete_social_link/',
         profile_view.delete_social_link,
         name='delete_social_link'
         ),
    path('best-articles/',
         index_content.best_articles,
         name='best_articles'
         ),
    path('best-authors/',
         index_content.best_authors,
         name='best_authors'
         ),
    path('favorites-authors/<username>/',
         index_content.favorites_authors,
         name='favorites_authors'
         ),
    path('<username>/',
         profile_view.profile,
         name='profile'
         ),
]
