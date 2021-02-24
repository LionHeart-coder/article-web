from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Exists, OuterRef
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


class PostQuerySet(models.QuerySet):
    def annotate_like(self, user):
        return self.annotate(
            liked=Exists(
                Like.objects.filter(user=user.id, post_id=OuterRef('id')).only('id')
            )
        )


class Post(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=80)
    preview_text = models.TextField(verbose_name='Описание поста', max_length=500)
    content = RichTextUploadingField()
    pub_date = models.DateTimeField('date published', auto_now_add=True,)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
    )
    group = models.ForeignKey(
        'Group',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа к которой привязывается пост',
    )
    preview_image = models.ImageField(
        verbose_name='Картинка для предпросмотра',
        upload_to='posts/preview/',
        help_text='Картинка к посту',
    )

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(
        max_length=200, verbose_name='Заголовок', help_text='Название группы',
    )
    slug = models.SlugField(
        max_length=256,
        unique=True,
        verbose_name='Слаг',
        help_text='Адрес для страницы с группой (только латиница)',
    )
    description = models.TextField(
        verbose_name='Описание', help_text='Описание группы'
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Здесь вы можете написать своё мнение по поводу поста',
    )
    created = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True,
    )
    reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.author


class Follow(models.Model):
    user = models.ForeignKey(
        User, related_name='follower', on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'author')

    def __str__(self):
        return f'{self.user} follow {self.author}'


class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} liked {self.post}'


class SocialLink(models.Model):
    LINKS_CHOICE = [
        ('youtube', 'Youtube'),
        ('twitter', 'Twitter'),
        ('vk', 'Вконтакте'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
    ]
    user = models.ForeignKey(User, related_name='social_links', on_delete=models.CASCADE)
    link_type = models.CharField(verbose_name='Тип ссылки', choices=LINKS_CHOICE, max_length=10)
    link = models.CharField(verbose_name='Ссылка', max_length=70)

    class Meta:
        unique_together = ('user', 'link_type')

    def __str__(self):
        return self.user
