from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignUpViewSet, TokenView, UserViewSet

router = DefaultRouter()
router.register(r'auth/signup', SignUpViewSet, basename='signup')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/token/', TokenView.as_view(), name='token'),
    path('users/<username>/',
         UserViewSet.as_view(
             {'get': 'retrieve', 'delete': 'destroy',
              'patch': 'update', 'post': 'create'}),
         name='user-me'),
    path('', include(router.urls)),
]
