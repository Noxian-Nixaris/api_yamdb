from rest_framework import serializers
from .models import User
import re
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, username):
        """
        Проверяет, что username содержит только допустимые символы.
        """
        pattern = r'^[\w.@+-]+\Z'
        if not re.search(pattern, username):
            raise serializers.ValidationError(
                "Username содержит не допустимые символы.")
        return username


class SignUpWithSameEmailSerializer(serializers.ModelSerializer):
    class Meta:
        pass


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)

    class Meta:
        fields = ('username', 'confirmation_code')


class CreateUpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError("Недопустимое имя пользователя.")
        return value

    def validate_bio(self, value):
        if value and len(value) > 200:
            raise serializers.ValidationError("Биография не может превышать 200 символов.")
        return value

    def validate_first_name(self, value):
        if value and len(value) > 150:
            raise serializers.ValidationError("Имя не может превышать 150 символов.")
        return value

    def validate_last_name(self, value):
        if value and len(value) > 150:
            raise serializers.ValidationError("Фамилия не может превышать 150 символов.")
        return value

    def update(self, instance, validated_data):
        validated_data.pop('role', None)  # Удаляем роль из данных, чтобы предотвратить её изменение
        return super().update(instance, validated_data)


class RetrieveUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name', 'bio', 'role')


class DeleteUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('username')
