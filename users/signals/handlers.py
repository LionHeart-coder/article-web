from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from users.utils import send_registration_mail

User = get_user_model()


def create_registration_email(sender, instance, created=False, **kwargs):
    if created and not instance.is_superuser:
        token = default_token_generator.make_token(instance)
        send_registration_mail(instance, token, instance.email)
