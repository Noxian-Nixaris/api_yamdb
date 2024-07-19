from rest_framework import status, generics
from rest_framework.response import Response
from .models import User
from django.core.mail import send_mail
from rest_framework.views import APIView
import random
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrReadOnly
from .serializers import (SignUpSerializer,
                          TokenSerializer,
                          CreateUpdateUserSerializer,
                          RetrieveUserSerializer,
                          DeleteUserSerializer)


def send_confirmation_email(email, code):
    send_mail(
        'Ваш код подтверждения',
        f'Ваш код подтверждения: {code}',
        'from@example.com',
        [email],
        fail_silently=False,
    )


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        existing_users = User.objects.filter(username=username)
        confirmation_code = random.randint(100000, 999999)
        user = User(username=username, email=email,
                    confirmation_code=confirmation_code)
        if username == 'me':
            return Response({'error': 'Недопустимое имя пользователя'},
                            status=status.HTTP_400_BAD_REQUEST)
        if existing_users.exists():
            return Response({'message': 'Код подтверждения отправлен'},
                            status=status.HTTP_200_OK)
        user.save()
        send_confirmation_email(user.email, user.confirmation_code)
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"user_id": user.id}, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if not username or not confirmation_code:
            return Response(
                {"error": "Username and confirmation code are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        if confirmation_code != 'expected_code':
            return Response(
                {"error": "Invalid confirmation code."},
                status=status.HTTP_400_BAD_REQUEST
            )


class CreateUserView(APIView):
    serializer_class = CreateUpdateUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def patch(self, request, username, *args, **kwargs):
        if username == 'me':
            user = request.user
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        if request.user != user and not request.user.is_superuser and request.user.role != 'admin':
            return Response({'error': 'Нет прав доступа'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CreateUpdateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        # Проверка прав доступа: только суперпользователи и администраторы могут создавать пользователей
        if request.user.is_superuser and request.user.role == 'admin':
            return Response({'error': 'Нет прав доступа'}, status=status.HTTP_403_FORBIDDEN)
        # Создание и валидация данных
        serializer = CreateUpdateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Создание нового пользователя
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, username=None):
        if username == 'me':
            user = request.user
        else:
            if not request.user.is_superuser and request.user.role != 'admin':
                return Response({'error': 'Нет прав доступа'}, status=status.HTTP_403_FORBIDDEN)
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CreateUpdateUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, username, *args, **kwargs):
        if username == 'me':
            return Response({'error': 'Метод не разрешен'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if not request.user.is_superuser and request.user.role != 'admin':
            return Response({'error': 'Нет прав доступа'},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(username=username)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'},
                            status=status.HTTP_404_NOT_FOUND)
