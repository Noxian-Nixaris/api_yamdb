import datetime as dt

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.relations import SlugRelatedField

from reviews.models import Title

User = get_user_model()


class TitleSerializer(serializers.ModelSerializer):

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError()
        return value

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category')
