from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, HotelOwner

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifier = data.get('email') or data.get('username')
        if not identifier or not data.get('password'):
            raise serializers.ValidationError("Email/Username and password are required")
        user = authenticate(
            username=identifier,
            password=data.get('password')
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("Account disabled")
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_hotel_owner')
        extra_kwargs = {
            'username': {'read_only': True},
            'email': {'required': True},
            'is_hotel_owner': {'read_only': True}
        }

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'email': {'required': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

class HotelOwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = HotelOwner
        fields = '__all__'
        read_only_fields = ('user',)