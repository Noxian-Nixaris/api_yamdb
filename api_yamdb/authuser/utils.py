from django.core.mail import send_mail
from random import randint


def send_confirmation_email(email, confirmation_code):
    """Функция отправки письма с кодом подтверждения."""
    confirmation_code = randint(100000, 999999)
    send_mail(
        'Ваш код подтверждения',
        f'Ваш код подтверждения: {confirmation_code}',
        'api_yamdb79@tutamail.com',
        [email],
        fail_silently=False,
    )
