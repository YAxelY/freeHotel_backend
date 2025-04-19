from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameAuthBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Handle empty username
        if not username:
            return None
            
        # Explicitly check both email and username
        try:
            if '@' in username:
                user = User.objects.get(email__iexact=username)
            else:
                user = User.objects.get(username__iexact=username)
                
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None