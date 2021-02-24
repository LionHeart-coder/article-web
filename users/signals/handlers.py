from django.contrib.auth import get_user_model

from users.utils import create_user_token, send_registration_mail

User = get_user_model()


def create_registration_email(sender, instance, created=False, **kwargs):
    print("Created:", created)
    if created:
        token = create_user_token(instance)
        send_registration_mail(instance, token, instance.email)
