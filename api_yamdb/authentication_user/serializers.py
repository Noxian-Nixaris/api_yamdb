from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied

from .models import User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
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
        existing_username = User.objects.filter(username=username).exists()
        if existing_username and confirmation_code:
            raise serializers.ValidationError('Не верный код подтверждения')
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user == instance:
            validated_data.pop('role', None)
        return super().update(instance, validated_data)

    def validate_destroy(self, request, *args, **kwargs):
        """Валидатор для проверки прав доступа при удалении пользователя."""
        username = kwargs.get('username', None)
        if username == 'me':
            raise MethodNotAllowed('Метод не разрешен')
        user = User.objects.filter(username=username).first()
        if user is None or (not request.user.is_superuser
                            and request.user.role != 'admin'):
            raise PermissionDenied('Нет прав доступа')
        return user

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        existing_email = User.objects.filter(email=email).exists()
        existing_username = User.objects.filter(username=username).exists()
        if existing_username:
            raise serializers.ValidationError('Имя пользователя уже занято')
        if existing_email:
            raise serializers.ValidationError('Почта уже занята')
        return data
