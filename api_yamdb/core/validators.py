import datetime

from django.core.exceptions import ValidationError


def year_check(year):
    if year > int(datetime.date.today().year):
        raise ValidationError()
