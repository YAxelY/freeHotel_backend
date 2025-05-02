from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from django.contrib.auth import get_user_model
from .models import User, HotelOwner
from .serializers import (
    LoginSerializer,
    UserSerializer,
    UserRegistrationSerializer,
    HotelOwnerSerializer
)
from .permissions import IsSelfOrAdmin, IsHotelOwnerOrAdmin
from rest_framework.permissions import AllowAny 

User = get_user_model()

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSelfOrAdmin]

    def get_serializer_class(self):
        return UserRegistrationSerializer if self.action == 'create' else super().get_serializer_class()

class HotelOwnerViewSet(viewsets.ModelViewSet):
    queryset = HotelOwner.objects.all()
    serializer_class = HotelOwnerSerializer
    permission_classes = [IsHotelOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        if not self.request.user.is_hotel_owner:
            self.request.user.is_hotel_owner = True
            self.request.user.save()

class CustomAuthToken(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            
            if not user.is_active:
                return Response(
                    {'error': 'Account disabled'}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        except serializers.ValidationError as e:
            return Response(
                {'error': 'Invalid credentials', 'details': str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        except Exception as e:
            return Response(
                {'error': 'Authentication failed', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response(UserSerializer(request.user).data)
    
    def put(self, request):
        serializer = UserSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class HotelOwnerRegistrationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if not request.user.is_hotel_owner:
            request.user.is_hotel_owner = True
            request.user.save()

        serializer = HotelOwnerSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)