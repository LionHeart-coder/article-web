from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.db import models

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('E-mail'), max_length=60, unique=True)
    username = models.CharField(_('Username'), max_length=50, unique=True)
    first_name = models.CharField(_('First name'), max_length=70)
    last_name = models.CharField(_('Last Name'), max_length=70)
    avatar = models.ImageField(_('Avatar'), upload_to='users/avatars', blank=True, null=True)

    date_joined = models.DateTimeField(_('Creation date'), auto_now_add=True)
    is_active = models.BooleanField(_('Active'), default=False)
    is_staff = models.BooleanField(_('Access to admin'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ For sending email to user """
        send_mail(subject, message, from_email, [self.email], **kwargs)
        
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

