# journal 1: Create Virtual Environment

Why? To isolate project dependencies from your system-wide Python installation.

## Create virtual environment named 'venv'

                 python -m venv venv

What this does: 

 python -m venv: Uses Python's built-in venv module

 venv: Creates a folder with Python interpreter copies and pip

## Activate Virtual Environment

Linux/Mac:

    source venv/bin/activate

What happens:

Your terminal prompt will show (venv) indicating the activated environment

All Python commands will now use this isolated environment

====================================================================

# journal 2: Install Dependencies

    pip install django djangorestframework django-cors-headers psycopg2-binary python-dotenv

Breakdown:

django: Core Django framework

djangorestframework: For building REST APIs

django-cors-headers: Handle Cross-Origin Resource Sharing (CORS) for React

psycopg2-binary: PostgreSQL database adapter

python-dotenv: Load environment variables from .env file

# journal 3: Create Django Project Structure

        django-admin startproject config .

File Structure Explanation:

    config/          # Project configuration
        __init__.py    # Marks as Python package
        settings.py    # All project settings
        urls.py        # Main URL routing
        wsgi.py        # Production deployment
    manage.py        # Django command-line utility


The trailing . means "create in current directory" instead of making a nested folder.


# journal 4:  Create Core App

    python manage.py startapp core

New files created:

        core/
            __init__.py
            admin.py       # Admin interface config
            apps.py        # App config
            models.py      # Database models
            tests.py       # Test classes
            views.py       # Request handlers

# journal 5: .gitignore File
Create .gitignore with this content:

    # Python
    __pycache__/
    *.py[cod]
    *.sqlite3
    *.env
    venv/

    # Django
    *.log
    *.pot
    *.pyc
    media/
    staticfiles/

    # IDE
    .vscode/
    .idea/

    # Database
    *.dump
    *.psql

    # Node/React (for later)
    node_modules/
    npm-debug.log*

    # Environment files
    .env
    .env.local
    .env.development
    .env.production

Why? To exclude temporary files, secrets, and build artifacts from version control.


# journal 6: Configure PostgreSQL (settings.py)

Modify config/settings.py:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'hotel_db',         # Database name
            'USER': 'hotel_user',       # Your PostgreSQL username
            'PASSWORD': 'securepass123', # Your PostgreSQL password
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

in case you used .env file:
    
    import os
    from dotenv import load_dotenv

    load_dotenv()  # Load environment variables from .env

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }
Before this works:

Create database in PostgreSQL:

    CREATE DATABASE hotel_db;
    CREATE USER hotel_user WITH PASSWORD 'securepass123';
    GRANT ALL PRIVILEGES ON DATABASE hotel_db TO hotel_user;

# journal 7: Configure Core App (settings.py)

Add to INSTALLED_APPS:

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'corsheaders',
        'core.apps.CoreConfig',  # Our custom app
    ]

Add middleware for CORS:

    MIDDLEWARE = [
        ...
        'corsheaders.middleware.CorsMiddleware',
    ]

# journal 8 : create models

    from django.db import models
    from django.contrib.auth.models import AbstractUser


    class User(AbstractUser):  # Inherit from Django's built-in user
        is_hotel_owner = models.BooleanField(default=False)
        email = models.EmailField(unique=True)
        created_at = models.DateTimeField(auto_now_add=True)

        class Meta:
            ordering = ['-created_at']


    class HotelOwner(models.Model):
        user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            primary_key=True
        )
        business_name = models.CharField(max_length=255)
        contact_number = models.CharField(max_length=20)


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

you are going to find a more details explaination at django_random_knowledge file

# journal 9: first migrations as test

    python manage.py makemigrations
    python manage.py migrate

then you gonna run into an error 

    ERRORS:
    auth.User.groups: (fields.E304) Reverse accessor 'Group.user_set' for 'auth.User.groups' clashes with reverse accessor for 'core.User.groups'.
            HINT: Add or change a related_name argument to the definition for 'auth.User.groups' or 'core.User.groups'.
    auth.User.user_permissions: (fields.E304) Reverse accessor 'Permission.user_set' for 'auth.User.user_permissions' clashes with reverse accessor for 'core.User.user_permissions'.
            HINT: Add or change a related_name argument to the definition for 'auth.User.user_permissions' or 'core.User.user_permissions'.
    core.User.groups: (fields.E304) Reverse accessor 'Group.user_set' for 'core.User.groups' clashes with reverse accessor for 'auth.User.groups'.
            HINT: Add or change a related_name argument to the definition for 'core.User.groups' or 'auth.User.groups'.
    core.User.user_permissions: (fields.E304) Reverse accessor 'Permission.user_set' for 'core.User.user_permissions' clashes with reverse accessor for 'auth.User.user_permissions'.
            HINT: Add or change a related_name argument to the definition for 'core.User.user_permissions' or 'auth.User.user_permissions'.


you just this to define  a custom group and permission for your user :

        # Add these two lines to resolve the conflict
        groups = models.ManyToManyField(
            Group,
            verbose_name=_('groups'),
            blank=True,
            help_text=_('The groups this user belongs to.'),
            related_name='core_user_groups',  # Unique related name
            related_query_name='user',
        )
        user_permissions = models.ManyToManyField(
            Permission,
            verbose_name=_('user permissions'),
            blank=True,
            help_text=_('Specific permissions for this user.'),
            related_name='core_user_permissions',  # Unique related name
            related_query_name='user',
        )

don't forget the imports :

    from django.contrib.auth.models import AbstractUser, Group, Permission
    from django.db import models
    from django.utils.translation import gettext_lazy as _


2. Why This Works

    Problem: Both default User and your custom User try to create reverse relationships named user_set for permissions/groups

    Solution:

        related_name='core_user_groups' creates unique reverse relation names

        related_name='core_user_permissions' does the same for permissions

    Key Change: Tells Django to use different names for these relationships


you still gonna run into an error

connect to hotel_db and give this permission to hotel_user

    GRANT USAGE ON SCHEMA public TO hotel_user;
    GRANT CREATE ON SCHEMA public TO hotel_user;

    ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO hotel_user;

    ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT ALL PRIVILEGES ON SEQUENCES TO hotel_user;


else :

    -- Check existing users
    \du

    -- If needed, create user with proper privileges
    CREATE USER hotel_user WITH PASSWORD 'securepass123' CREATEDB CREATEROLE;

    -- Grant privileges
    ALTER USER hotel_user WITH SUPERUSER;

---

        -- Grant all privileges on database
    GRANT ALL PRIVILEGES ON DATABASE hotel_db TO hotel_user;

    -- Grant privileges on migrations table
    GRANT ALL PRIVILEGES ON TABLE django_migrations TO hotel_user;

    -- If using existing tables
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hotel_user;

in case is still sturborn :

    -- Drop and recreate database
    DROP DATABASE IF EXISTS hotel_db;
    CREATE DATABASE hotel_db OWNER hotel_user;


# journal 10 specify the  model to use for auth

for testing add:

    # settings.py
    AUTH_USER_MODEL = 'core.User'


# journal 11 : check app calling order

you may have to  call core.apps.CoreConfig before Django.contrib.auth 
since auth needs core_user to be ready .

# journal 12 : added custom auth logic 

 create core.backends.Py

    from django.contrib.auth import get_user_model

    User = get_user_model()

    class EmailOrUsernameAuthBackend:
        def authenticate(self, request, username=None, password=None, **kwargs):
            if '@' in username:
                kwargs = {'email': username}
            else:
                kwargs = {'username': username}
            
            try:
                user = User.objects.get(**kwargs)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None

        def get_user(self, user_id):
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None


add this list to settings


    AUTHENTICATION_BACKENDS = [
        'core.backends.EmailOrUsernameAuthBackend',
        'django.contrib.auth.backends.ModelBackend'
    ]

# journal 13: serializers

    from rest_framework import serializers
    from django.contrib.auth import authenticate
    from .models import User

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

# journal 14 : views 
    from django.shortcuts import render

    from rest_framework.views import APIView
    from rest_framework.response import Response
    from rest_framework import status
    from rest_framework.authtoken.models import Token
    from .serializers import LoginSerializer, UserSerializer

    class LoginView(APIView):
        def post(self, request):
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })

    class LogoutView(APIView):
        def post(self, request):
            request.user.auth_token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
# journal 15: updates urls.py

    from django.urls import path
    from .views import LoginView, LogoutView

    urlpatterns = [
        path('login/', LoginView.as_view(), name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),
    ]

# journal 16: updates config.urls.py

    from django.urls import include, path

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/', include('core.urls')),  
    ]


# journal 17 : re-structuring (for better maintenance)

    python manage.py startapp users
    python manage.py startapp hotels
    python manage.py startapp search

