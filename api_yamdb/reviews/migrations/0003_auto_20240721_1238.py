# Generated by Django 3.2 on 2024-07-21 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_genre_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(to='reviews.Genre'),
        ),
        migrations.DeleteModel(
            name='GenreTitle',
        ),
    ]
