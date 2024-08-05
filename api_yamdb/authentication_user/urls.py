from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignUpViewSet, TokenView, UserViewSet

router_v1 = DefaultRouter()
router_v1.register('v1/auth/signup', SignUpViewSet, basename='signup')
router_v1.register('v1/users', UserViewSet, basename='users')
router_v1.register('v1/users/<username>', UserViewSet, basename='username')

urlpatterns = [
    path('v1/auth/token/', TokenView.as_view(), name='token'),
    path('', include(router_v1.urls)),
]
