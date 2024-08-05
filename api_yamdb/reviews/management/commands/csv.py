import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import (
    Category, Genre, GenreTitle, Title, Review, Comments
)

User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("csv_to_db")

    def handle(self, *args, **options):
        models_list = (
            User, Category, Genre, Title, Review, Comments, GenreTitle
        )
        file_list = (
            'users', 'category', 'genre', 'title',
            'review', 'comments', 'genretitle'
        )
        for i in range(7):
            with open(
                f'static/data/{file_list[i]}.csv', newline='', encoding='utf-8'
            ) as csvfile:
                reader = csv.DictReader(csvfile)
                # for row in reader:
                #     print(row)
                instances = (models_list[i](**row) for row in reader)

                models_list[i].objects.bulk_create(instances)
