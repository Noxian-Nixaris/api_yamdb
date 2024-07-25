from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role']

    def validate_role(self, data):
        request = self.context.get('request')
        user = request.data
        if 'role' not in user:
            return data
        if request.user.role not in ['admin']:
            raise serializers.ValidationError("Изменение роли запрещено.")
        return data


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email',
                  'first_name', 'last_name', 'bio', 'role']


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError("Недопустимое имя пользователя.")
        return username


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
