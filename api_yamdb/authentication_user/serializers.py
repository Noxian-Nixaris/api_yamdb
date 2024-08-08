from rest_framework import serializers

from authentication_user.models import User
from core.constants import (
    MAX_LENGTH, EMAIL_MAX_LENGTH,
    PATTERN_VALIDATOR, username_not_me_validator,
)


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH,
        validators=[PATTERN_VALIDATOR, username_not_me_validator]
    )
    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH,
    )

    class Meta:
        fields = ('email', 'username')

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        existing_email = User.objects.filter(email=email).exists()
        existing_username = User.objects.filter(username=username).exists()
        if existing_email and not existing_username:
            raise serializers.ValidationError('Почта уже занята')
        if existing_username and not existing_email:
            raise serializers.ValidationError('Имя пользователя уже занято')
        return data


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        confirmation_code = data.get('confirmation_code')
        username = data.get('username')
        user = User.objects.filter(username=username).first()
        if user and confirmation_code != user.confirmation_code:
            raise serializers.ValidationError('Неверный код подтверждения')
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']
