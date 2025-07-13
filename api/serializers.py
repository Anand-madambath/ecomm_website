from rest_framework import serializers
from accounts.models import Product, Category, Review, CustomUser
from django.contrib.auth.password_validation import validate_password

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'
    def validate(self, data):
        user = self.context['request'].user
        product = data['product']
        rating = data['rating']
        if Review.objects.filter(product=product, user=user).exists():
            raise serializers.ValidationError("You have already reviewed this product.")
        if rating < 1 or rating > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'role')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user
