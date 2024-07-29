from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.mixins import (RetrieveModelMixin, CreateModelMixin,
                                   UpdateModelMixin, ListModelMixin,
                                   DestroyModelMixin)
from random import randint

from .models import User
from .utils import send_confirmation_email
from .serializers import (UserSerializer, SignUpSerializer,
                          CreateUserSerializer, TokenSerializer)


class UserViewSet(GenericViewSet, RetrieveModelMixin, CreateModelMixin,
                  UpdateModelMixin, ListModelMixin, DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'

    def get_object(self):
        """Получение модели пользователя."""
        username = self.kwargs.get('username', None)
        if username == 'me':
            return self.request.user
        return super().get_object()

    def list(self, request, *args, **kwargs):
        """Получение списка пользователей."""
        if not request.user.is_superuser and request.user.role != 'admin':
            return Response({'Ошибка': 'Нет прав доступа'},
                            status=status.HTTP_403_FORBIDDEN)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Создание пользователя."""
        serializer = CreateUserSerializer(data=request.data,
                                          context={'request': request})
        user = request.user
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if user and user.is_authenticated and user.is_staff:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """Обработка GET запросов."""
        user = self.get_object()
        if user != request.user and request.user.role != 'admin':
            return Response({'Ошибка': 'Нет прав доступа'},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """Обработка PATCH запросов."""
        user = self.get_object()
        if user == self.request.user and kwargs.get('username') == 'me':
            serializer = self.serializer_class(user, data=request.data,
                                               partial=True,
                                               context={'request': request})
        else:
            if not request.user.is_superuser and request.user.role != 'admin':
                return Response({'Ошибка': 'Нет прав доступа'},
                                status=status.HTTP_403_FORBIDDEN)
            serializer = self.serializer_class(user, data=request.data,
                                               partial=True,
                                               context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.errors, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Удаление пользователя."""
        if kwargs.get('username') == 'me':
            return Response({'Ошибка': 'Метод не разрешен'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        if not request.user.is_superuser and request.user.role != 'admin':
            return Response({'Ошибка': 'Нет прав доступа'},
                            status=status.HTTP_403_FORBIDDEN)
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SignUpViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        """Регистрация пользователя."""
        serializer = SignUpSerializer(data=request.data,
                                      context={'request': request})
        email = request.data.get('email')
        username = request.data.get('username')
        confirmation_code = str(randint(100000, 999999))
        existing_username = User.objects.filter(username=username).exists()
        existing_email = User.objects.filter(email=email).exists()
        response_data = {'email': email,
                         'username': username,
                         'confirmation_code': confirmation_code}
        if serializer.is_valid():
            user = serializer.save()
            user.confirmation_code = confirmation_code
            user.save()
            # send_confirmation_email(email, confirmation_code)
            return Response(response_data, status=status.HTTP_200_OK)
        if existing_username and existing_email:
            # send_confirmation_email(email, confirmation_code)
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        """Создание токена."""
        serializer = TokenSerializer(data=request.data,
                                     context={'request': request})
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            if confirmation_code != existing_user.confirmation_code:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(existing_user)
            token = {'refresh': str(refresh),
                     'access': str(refresh.access_token)}
            return Response(token, status=status.HTTP_200_OK)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            token = {'refresh': str(refresh),
                     'access': str(refresh.access_token)}
            if username is not None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(token, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
