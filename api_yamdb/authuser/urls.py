from django.urls import path
from .views import SignUpView, TokenView, UserView

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view(), name='token'),
    path('v1/users/', UserView.as_view(), name='users'),
]
