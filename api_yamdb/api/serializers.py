import datetime as dt

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from reviews.models import Category, Title

User = get_user_model()


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    genre = 1

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError()
        return value

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genre')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
