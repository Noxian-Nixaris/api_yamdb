from django.contrib import admin
from .models import Category, Comments, Genre, Title, Review


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name', 'slug')


class CommentsAdmin(admin.ModelAdmin):
    model = Comments
    list_display = ('text', 'review', 'pub_date', 'author')


class GenreAdmin(admin.ModelAdmin):
    model = Genre
    list_display = ('name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    model = Title
    list_display = ('name', 'year', 'category', 'description')


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('text', 'title', 'pub_date', 'author', 'score')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
