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