from django.urls import include, path
from rest_framework import routers

from api.views import CategoryViewSet, TitleViewSet


router_v1 = routers.DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')

urlpatterns_v1 = [
    path('', include(router_v1.urls))
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1))
]
