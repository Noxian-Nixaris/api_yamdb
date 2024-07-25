from django.core.mail import send_mail
from random import randint


def send_confirmation_email(email, code):
    """Функция отправки письма с кодом подтверждения."""
    code = randint(100000, 999999)
    send_mail(
        'Ваш код подтверждения',
        f'Ваш код подтверждения: {code}',
        'from@example.com',
        [email],
        fail_silently=False,
    )


def confirmation_code_generator():
    """Функция генерации кода подтверждения."""
    code = randint(100000, 999999)
    return code
