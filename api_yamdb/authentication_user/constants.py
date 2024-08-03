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
