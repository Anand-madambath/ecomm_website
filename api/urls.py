from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CategoryViewSet, ReviewViewSet, UserViewSet,
    RegisterView, LogoutView, CustomLoginView
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='api-register'),
    path('login/', CustomLoginView.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
