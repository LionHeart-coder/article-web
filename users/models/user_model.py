from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Почта', max_length=60, unique=True)
    username = models.CharField('Имя пользователя', max_length=50, unique=True)
    first_name = models.CharField('Имя', max_length=70)
    last_name = models.CharField('Фамилия', max_length=70)
    avatar = models.ImageField('Аватар пользователя',
                               upload_to='users/avatars/',
                               null=True,
                               blank=True,
                               )
    about_author = models.TextField(verbose_name='О себе', max_length=700)

    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)

    email_timestamp = models.IntegerField('Переотправление письма', default=0, help_text='Время до повторной отправки письма')

    is_active = models.BooleanField('Аккаунт активирован', default=False)
    is_staff = models.BooleanField('Админ', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ For sending email to user """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def update_email_timestamp(self):
        self.email_timestamp = int(datetime.now().timestamp() + 60)
        # TODO оптимизировать сохранение
        self.save()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
