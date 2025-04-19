from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import HotelOwner, User

from .models import Hotel, Room

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            username=data.get('username_or_email'),
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
            'username': {'read_only': True},  # Empêche la modification
            'email': {'required': True}
        }
        



class HotelSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Hotel
        fields = '__all__'
        read_only_fields = ('owner', 'rating')

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ('hotel',)
        extra_kwargs = {
            'room_number': {'required': False},
            'room_type': {'required': False},
            'capacity': {'required': False}
        }
        


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_hotel_owner')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_hotel_owner=validated_data.get('is_hotel_owner', False)
        )
        return user

class HotelOwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = HotelOwner
        fields = '__all__'
        read_only_fields = ('user',)