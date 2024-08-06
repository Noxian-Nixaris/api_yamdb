import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import (
    Category, Genre, GenreTitle, Title, Review, Comments
)
from core.constants import STATIC_PASS

User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("csv_to_db")

    def handle(self, *args, **options):
        transfer_dict = {
            'users': User,
            'category': Category,
            'genre': Genre,
            'title': Title,
            'review': Review,
            'comments': Comments,
            'genretitle': GenreTitle
        }
        for file in transfer_dict:
            with open(
                f'{STATIC_PASS}{file}.csv', newline='', encoding='utf-8'
            ) as csvfile:
                reader = csv.DictReader(csvfile)
                instances = (transfer_dict[file](**row) for row in reader)
                transfer_dict[file].objects.bulk_create(instances)
