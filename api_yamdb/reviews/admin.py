from django.contrib import admin

from reviews.models import Category, Comments, Genre, Review, Title


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
    list_display = ('name', 'year', 'category', 'description', 'get_genre')
    list_editable = ('category',)

    def get_genre(self, obj):
        return [genre.name for genre in obj.genre.all()]


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('text', 'title', 'pub_date', 'author', 'score')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
