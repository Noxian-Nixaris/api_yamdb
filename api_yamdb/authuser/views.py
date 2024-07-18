from rest_framework import status, generics
from rest_framework.response import Response
from .models import User
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        if username == 'me':
            return Response({'error': 'Не допустимое имя пользователя'},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'message': 'Пользователь уже существует'},
                            status=status.HTTP_200_OK)
        if request.user.is_staff and serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = TokenSerializer

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.is_staff:
            return Response(serializer.data, status=status.HTTP_200_OK)
        if not serializer.is_valid():
            return Response(serializer.data,
                            status=status.HTTP_400_BAD_REQUEST)


class UserView(generics.CreateAPIView):
    serializer_class = UserSerializer
