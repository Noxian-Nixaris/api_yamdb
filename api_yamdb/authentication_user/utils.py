from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def send_confirmation_email(user):
    """Функция отправки письма с кодом подтверждения."""
    token = default_token_generator.make_token(user)
    email = user.email
    send_mail(
        'Ваш код подтверждения',
        f'Ваш код подтверждения: {token}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return token
