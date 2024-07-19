from django.urls import path
from .views import SignUpView, TokenView, CreateUserView

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view(), name='token'),
    path('v1/users/', CreateUserView.as_view(), name='users'),
    path('v1/user/', CreateUserView.as_view(), name='user'),
    path('v1/users/<str:username>/',
         CreateUserView.as_view(), name='user-detail'),
    path('v1/user/me/', CreateUserView.as_view(), name='detail_user'),
]
