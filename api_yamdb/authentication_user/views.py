from django.shortcuts import get_object_or_404
from rest_framework import status, filters, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

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
        email = request.data.get('email')
        username = request.data.get('username')
        if serializer.is_valid(raise_exception=True):
            user, created = User.objects.get_or_create(email=email,
                                                       username=username)
            send_confirmation_email(user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        """Создание токена."""
        serializer = TokenSerializer(data=request.data,
                                     context={'request': request})
        username = request.data.get('username')
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(User, username=username)
            refresh = RefreshToken.for_user(user)
            token = {'refresh': str(refresh),
                     'access': str(refresh.access_token)}
            return Response(token, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperuser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False, methods=['get', 'patch'], url_path='me',
            permission_classes=[IsAuthenticated])
    def update_me(self, request, *args, **kwargs):
        """Обработка GET и PATCH запросов для текущего пользователя."""
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True,
                                    context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(role=self.request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
