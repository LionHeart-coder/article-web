from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

handler404 = 'posts.views.base_view.page_not_found'  # noqa
handler500 = 'posts.views.base_view.server_error'  # noqa

urlpatterns = [
    path('about-author/', views.flatpage, {'url': '/about-author/'}, name='about_author'),
    path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name='about_spec'),
    path('about/', include('django.contrib.flatpages.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin-page/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('posts.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
