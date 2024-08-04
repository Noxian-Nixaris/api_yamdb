from rest_framework import status, filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import User
from .permissions import IsAdminOrSuperuser
from .serializers import UserSerializer, SignUpSerializer, TokenSerializer
from .utils import send_confirmation_email


class SignUpViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        """Регистрация пользователя."""
        serializer = SignUpSerializer(data=request.data,
                                      context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            send_confirmation_email(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise ValidationError(serializer.errors)


class TokenView(APIView):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        """Создание токена."""
        serializer = TokenSerializer(data=request.data,
                                     context={'request': request})
        username = request.data.get('username')
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            token = {'refresh': str(refresh),
                     'access': str(refresh.access_token)}
            if username is not None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(token, status=status.HTTP_200_OK)
        raise ValidationError(serializer.errors)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperuser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    def update(self, request, *args, **kwargs):
        """Обработка PATCH запросов."""
        if kwargs.get('username') == 'me':
            user = request.user
        else:
            user = self.get_object()
            if not request.user.is_superuser and request.user.role != 'admin':
                raise PermissionDenied('У вас нет прав для изменения данных')
        serializer = UserSerializer(user, data=request.data,
                                    partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Удаление пользователя."""
        serializer = self.get_serializer()
        user = serializer.validate_destroy(request, *args, **kwargs)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        """Обработка GET запросов для получения данных пользователя."""
        if kwargs.get('username') == 'me':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        return super().retrieve(request, *args, **kwargs)
