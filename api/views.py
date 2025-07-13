from rest_framework import viewsets, permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied


from accounts.models import Product, Category, Review, CustomUser
from .serializers import (
    ProductSerializer, CategorySerializer, ReviewSerializer,
    UserSerializer, RegisterSerializer
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            raise PermissionDenied("Only admin users can view this.")
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            raise PermissionDenied("Only admin users can view this.")
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            raise PermissionDenied("Only admin users can create users.")
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            raise PermissionDenied("Only admin users can update users.")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            raise PermissionDenied("Only admin users can delete users.")
        return super().destroy(request, *args, **kwargs)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username,
            'role': token.user.role
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
