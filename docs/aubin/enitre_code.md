"""
Django settings for config project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings (à adapter pour la production)
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-for-dev')  # Utilisation d'une variable d'environnement
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    # Apps métier
    'users.apps.UsersConfig',

    
    # Apps Django de base
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Packages tiers
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    
    # Apps métier
    'hotels.apps.HotelsConfig',
    'search.apps.SearchConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Placé avant CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Ajout d'un répertoire global de templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER').strip(),  # Add .strip() to remove whitespace
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # Longueur minimale configurable
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'  # Français
TIME_ZONE = 'Europe/Paris'  # Fuseau horaire
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Pour la collecte des fichiers statiques
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'users.User'

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'users.backends.EmailOrUsernameAuthBackend',
    'django.contrib.auth.backends.ModelBackend'
]

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',  # Plus flexible
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# CORS Settings (à adapter en production)
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Seulement en développement
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


# .env
DB_NAME=hotel_db
DB_USER=hotel_user  # Remove comment here
DB_PASSWORD=securepass123
DB_HOST=localhost
DB_PORT=5432

from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Hotel, Room
from users.models import User, HotelOwner

class HotelModelTests(TestCase):
    def setUp(self):
        owner_user = User.objects.create_user(
            email='hotelowner@test.com',
            password='testpass',
            is_hotel_owner=True
        )
        self.owner = HotelOwner.objects.create(
            user=owner_user,
            business_name="Grand Hotels",
            contact_number="+11111111"
        )

    # Ajouter ici les tests Hotel...

class RoomModelTests(TestCase):
    def setUp(self):
        owner_user = User.objects.create_user(
            email='rooms@test.com',
            password='testpass',
            is_hotel_owner=True
        )
        owner = HotelOwner.objects.create(
            user=owner_user,
            business_name="Room Experts",
            contact_number="+22222222"
        )
        self.hotel = Hotel.objects.create(
            owner=owner,
            name="Room Test Hotel",
            location="Test",
            description="Test",
            rating=4.0
        )

    # Ajouter ici les tests Room...
    
    from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Hotel

class HotelAPITests(APITestCase):
    def test_hotel_list(self):
        url = reverse('hotel-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        
        from django.contrib import admin
from .models import Hotel, Room

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    inlines = [RoomInline]
    list_display = ('name', 'location', 'owner', 'rating')
    list_filter = ('location', 'rating')
    search_fields = ('name', 'location')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'hotel', 'room_type', 'price_per_night', 'is_available')
    list_filter = ('room_type', 'is_available')
    search_fields = ('room_number', 'hotel__name')
    
    from django.apps import AppConfig


class HotelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotels'

from django.db import models
from django_filters import rest_framework as filters
from .models import Hotel

class HotelFilter(filters.FilterSet):
    amenities = filters.CharFilter(method='filter_amenities')

    class Meta:
        model = Hotel
        fields = {
            'name': ['exact', 'icontains'],
            'location': ['exact', 'icontains'],
            'rating': ['gte', 'lte'],
        }
        filter_overrides = {
            models.JSONField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {'lookup_expr': 'icontains'}
            }
        }

    def filter_amenities(self, queryset, name, value):
        return queryset.filter(amenities__contains=[value])
        
        from django.db import models

from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group  ,Permission

from django.utils.translation import gettext_lazy as _

from users.models import HotelOwner




class Hotel(models.Model):
    owner = models.ForeignKey(HotelOwner, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.FloatField(default=0.0)
    amenities = models.JSONField(default=list)  
    
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    
    from rest_framework import permissions
from .models import Hotel, Room

class IsHotelOwner(permissions.BasePermission):
    """Vérifie si l'utilisateur est propriétaire de la ressource"""
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Hotel):
            return obj.owner.user == request.user
        if isinstance(obj, Room):
            return obj.hotel.owner.user == request.user
        return False

class CanManageHotel(permissions.BasePermission):
    """Autorise la création uniquement aux propriétaires d'hôtel"""
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_authenticated and request.user.is_hotel_owner
        return True
        
        from rest_framework import serializers
from .models import Hotel, Room

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
        
        from django.urls import path
from .views import HotelListCreateView, HotelDetailView, RoomListCreateView, RoomDetailView

app_name = 'hotels'

urlpatterns = [
    path('hotels/', HotelListCreateView.as_view(), name='hotel-list'),
    path('hotels/<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    path('hotels/<int:hotel_id>/rooms/', RoomListCreateView.as_view(), name='room-list'),
    path('hotels/<int:hotel_id>/rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
]

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Hotel, Room
from .serializers import HotelSerializer, RoomSerializer
from .permissions import CanManageHotel, IsHotelOwner
from .filters import HotelFilter

class HotelListCreateView(generics.ListCreateAPIView):
    serializer_class = HotelSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'location', 'description']
    filterset_class = HotelFilter
    permission_classes = [CanManageHotel]

    def get_queryset(self):
        queryset = Hotel.objects.all()
        if self.request.query_params.get('has_available_rooms'):
            queryset = queryset.filter(rooms__is_available=True).distinct()
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.hotelowner)

class HotelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsHotelOwner]

class RoomListCreateView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsHotelOwner]

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        return Room.objects.filter(hotel__id=hotel_id)

    def perform_create(self, serializer):
        hotel = get_object_or_404(Hotel, id=self.kwargs['hotel_id'])
        serializer.save(hotel=hotel)

class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsHotelOwner]

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        return Room.objects.filter(hotel__id=hotel_id)
        
        from django.test import TestCase
from hotels.models import Hotel

class SearchTests(TestCase):
    def test_hotel_search(self):
        Hotel.objects.create(name="Grand Hotel", location="Paris")
        results = Hotel.objects.filter(name__icontains="Grand")
        self.assertEqual(results.count(), 1)
        
        
        from django.contrib import admin

# Register your models here.

from django.apps import AppConfig


class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'

from django.db import models  # Importer le module models de Django
from django_filters import rest_framework as filters
from hotels.models import Hotel  # Importer explicitement le modèle Hotel


class HotelSearchFilter(filters.FilterSet):
    q = filters.CharFilter(method='custom_search')

    class Meta:
        model = Hotel
        fields = ['q']

    def custom_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(name__icontains=value) |
            models.Q(location__icontains=value) |
            models.Q(description__icontains=value)
        )
        
        from django.db import models

# Create your models here.

# search/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Ajouter vos routes de recherche ici
    # Exemple : path('hotels/', views.HotelSearchView.as_view()),
]
# search/views.py
from django_filters.rest_framework import FilterSet, CharFilter  # Import correct
from rest_framework import generics
from hotels.models import Hotel
from django.contrib.postgres.search import SearchVector

class HotelSearchFilter(FilterSet):
    search = CharFilter(method='full_text_search')  # Plus de référence à 'filters'

    def full_text_search(self, queryset, name, value):
        return queryset.annotate(
            search=SearchVector('name', 'location', 'description')
        ).filter(search=value)

class HotelSearchView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    filterset_class = HotelSearchFilter
    
    from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import HotelOwner

User = get_user_model()

class UserModelTests(TestCase):
    def test_create_regular_user(self):
        user = User.objects.create_user(
            email='guest@test.com',
            password='testpass123'
        )
        self.assertEqual(user.email, 'guest@test.com')
        self.assertFalse(user.is_hotel_owner)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

class HotelOwnerModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='owner@test.com',
            password='testpass',
            is_hotel_owner=True
        )

    def test_hotel_owner_creation(self):
        owner = HotelOwner.objects.create(
            user=self.user,
            business_name="Luxury Stays",
            contact_number="+123456789"
        )
        self.assertEqual(owner.user.email, 'owner@test.com')
        self.assertEqual(owner.business_name, "Luxury Stays")
        self.assertEqual(str(owner), "Luxury Stays")
        
        from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from users.models import HotelOwner

User = get_user_model()

class PermissionTests(APITestCase):
    def setUp(self):
        self.owner_user = User.objects.create_user(
            email='owner@test.com',
            password='testpass',
            is_hotel_owner=True
        )
        HotelOwner.objects.create(
            user=self.owner_user,
            business_name="Test Business",
            contact_number="+111111111"
        )

    def test_hotel_owner_permissions(self):
        self.client.force_authenticate(user=self.owner_user)
        url = reverse('hotels:hotel-list')
        response = self.client.post(url, {
            'name': 'Test Hotel',
            'address': '123 Test Street',
            'description': 'Test description'
        })
        self.assertEqual(response.status_code, 201)

    def test_regular_user_permissions(self):
        regular_user = User.objects.create_user(
            email='user@test.com', 
            password='testpass'
        )
        self.client.force_authenticate(user=regular_user)
        url = reverse('hotels:hotel-list')
        response = self.client.post(url, {
            'name': 'Unauthorized Hotel',
            'address': '456 Blocked Ave'
        })
        self.assertEqual(response.status_code, 403)
        
        from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewsTests(APITestCase):
    def test_user_registration(self):
        url = reverse('user-registration')
        data = {
            'email': 'test@example.com',
            'password': 'ComplexPass123!',
            'username': 'testuser'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

    def test_user_login(self):
        User.objects.create_user(email='test@example.com', password='testpass')
        url = reverse('api-token-auth')
        data = {
            'username_or_email': 'test@example.com',
            'password': 'testpass'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
    
    
    # test_views.py
def test_hotel_owner_registration(self):
    user = User.objects.create_user(email='test@example.com', password='testpass')
    self.client.force_authenticate(user=user)
    
    url = reverse('hotel-owner-registration')
    data = {
        'business_name': 'Test Hotel',
        'contact_number': '+1234567890'
    }
    
    response = self.client.post(url, data)
    self.assertEqual(response.status_code, 201)
    self.assertTrue(user.is_hotel_owner)
    
    from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, HotelOwner

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'is_hotel_owner',
                'groups',
                'user_permissions'
            ),
        }),
        ('Dates', {'fields': ('last_login', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username', 'is_staff', 'is_hotel_owner')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_hotel_owner')
    search_fields = ('email', 'username')
    ordering = ('-created_at',)
    readonly_fields = ('last_login', 'created_at')

@admin.register(HotelOwner)
class HotelOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'contact_number')
    search_fields = ('user__email', 'business_name')

admin.site.register(User, CustomUserAdmin)

from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameAuthBackend:
    """
    Authentifie les utilisateurs par email ou nom d'utilisateur
    Gère la casse insensible et les erreurs multiples
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        try:
            user = User.objects.get(
                Q(username__iexact=username) | 
                Q(email__iexact=username)
            )
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # Gestion avancée des doublons
            return User.objects.filter(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            ).first()
        except Exception as e:
            # Loguer l'erreur pour le monitoring
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
            
            from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        if not email and not username:
            raise ValueError(_('At least email or username must be set'))
        
        if email:
            email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(
            email=email,
            password=password,
            **extra_fields
        )

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True
    )
    email = models.EmailField(
        _('email address'), 
        unique=True, 
        blank=False,
        null=False
    )
    is_hotel_owner = models.BooleanField(_('hotel owner status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)

    # Relations
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_set',
        related_query_name='user',
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        if not self.email and not self.username:
            raise ValidationError(_('At least email or username must be set'))

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']

    def __str__(self):
        return self.email

class HotelOwner(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    business_name = models.CharField(_('business name'), max_length=255)
    contact_number = models.CharField(_('contact number'), max_length=20)

    def __str__(self):
        return self.business_name
        
        from rest_framework import permissions
from hotels.models import Hotel, Room  

class IsHotelOwner(permissions.BasePermission):
    """Vérifie si l'utilisateur est le propriétaire de l'hôtel"""
    def has_object_permission(self, request, view, obj):
        # Pour les Hôtels
        if isinstance(obj, Hotel):
            return obj.owner.user == request.user
        
        # Pour les Chambres (via la relation Hotel)
        if isinstance(obj, Room):
            return obj.hotel.owner.user == request.user
        
        return False
    
# permissions.py
class CanManageHotel(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_hotel_owner
        return True


class IsSelfOrAdmin(permissions.BasePermission):
    """Allow users to edit their own profile"""
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff

class IsHotelOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or (request.user.is_hotel_owner and obj.user == request.user)
        
        from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, HotelOwner

class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

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
        
        from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    HotelOwnerViewSet,
    LoginView,
    LogoutView,
    UserMeView,
    CustomAuthToken,
    HotelOwnerRegistrationView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'hotel-owners', HotelOwnerViewSet, basename='hotelowner')

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'create'}), name='user-registration'),
    path('register/hotel-owner/', HotelOwnerRegistrationView.as_view(), name='hotel-owner-registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('token-auth/', CustomAuthToken.as_view(), name='api-token-auth'),
    path('', include(router.urls)),
]

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

User = get_user_model()

class LoginView(APIView):
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