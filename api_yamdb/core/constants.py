import datetime

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254
CONFIRMATION_CODE_MAX_LENGTH = 6
ROLE_MAX_LENGTH = 26
ROLE_USER = 'user'
ROLE_MODERATOR = 'moderator'
ROLE_ADMIN = 'admin'

PATTERN_VALIDATOR = RegexValidator(
    regex=r'^[\w.@+-]+\Z',
    message='Имя пользователя недопустимо'
)


def username_not_me_validator(username):
    if username == 'me':
        raise ValidationError('Недопустимое имя пользователя.')


NAME_MAX_LENGTH = 256
SLUG_MAX_LENGTH = 50
PAGE_SIZE = 15
CHOICES_SCORE = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10')
)
DISPLAY_LENGTH = 30
MIN_SCORE = 1
MAX_SCORE = 10
ACTUAL_YEAR = int(datetime.date.today().year)
STATIC_PASS = 'static/data/'
