from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string


def create_user_token(current_user):
    token = default_token_generator.make_token(current_user)
    return token


def send_registration_mail(recipient, token, email):
    current_domain = settings.CURRENT_DOMAIN
    protocol = "https" if settings.IS_SECURE else "http"
    message = render_to_string(
        'users/activation_account_mail.html',
        {'url': f'{protocol}://{current_domain}/auth/check-user-token?token={token}&email={email}'}
    )
    recipient.email_user(
        'Подтвердите вашу почту',
        'Подтвердите вашу почту',
        settings.EMAIL_HOST_USER,
        html_message=message,
    )
    recipient.update_email_timestamp()

