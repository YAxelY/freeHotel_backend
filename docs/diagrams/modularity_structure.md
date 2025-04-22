Voici la décomposition en applications Django recommandée pour votre projet, avec une explication détaillée :

### 1. Application `users` (Gestion des utilisateurs)
**Responsabilités** :
- Authentification (login/logout)
- Gestion des profils utilisateur
- Rôles (Guest, HotelOwner, Admin)
- Permissions

**Contenu** :
```python
# models.py
class User(AbstractBaseUser, PermissionsMixin):
    # ... champs existants

class HotelOwner(models.Model):
    user = models.OneToOneField(User, ...)
    # ... champs métier
```

**Avantages** :
- Centralise toute la logique d'authentification
- Gestion cohérente des différents types d'utilisateurs
- Permissions personnalisées regroupées

### 2. Application `hotels` (Gestion des établissements)
**Responsabilités** :
- Création/modification des hôtels
- Gestion des chambres
- Disponibilité en temps réel

**Contenu** :
```python
# models.py
class Hotel(models.Model):
    owner = models.ForeignKey('users.HotelOwner', ...)
    # ... champs existants

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, ...)
    # ... champs existants
```

**Avantages** :
- Séparation claire des entités métier
- Facilite l'ajout de fonctionnalités spécifiques
- Optimisation des requêtes liées aux hôtels

### 3. Application `search` (Recherche avancée)
**Responsabilités** :
- Moteur de recherche plein texte
- Filtres complexes
- Intégration avec Elasticsearch/Solr (optionnel)

**Contenu** :
```python
# filters.py
class HotelFilter(filters.FilterSet):
    # ... logique existante améliorée

# views.py
class HotelSearchView(SearchView):
    # ... intégration recherche avancée
```

**Avantages** :
- Performance optimisée pour la recherche
- Facile à maintenir et améliorer
- Peut devenir un microservice indépendant

### 4. Application `bookings` (Réservations et paiements)
**Responsabilités** :
- Gestion des réservations
- Intégration de paiement
- Calendrier de disponibilité

**Contenu** (à développer) :
```python
# models.py
class Booking(models.Model):
    user = models.ForeignKey('users.User', ...)
    room = models.ForeignKey('hotels.Room', ...)
    # ... champs de réservation

class Payment(models.Model):
    # ... logique de paiement
```

**Avantages** :
- Sécurité renforcée pour les transactions
- Isolation des données sensibles
- Facilité d'intégration avec des API externes

### 5. Application `reviews` (Avis et notations)
**Responsabilités** :
- Gestion des avis clients
- Modération des commentaires
- Système de notation

**Contenu** (à développer) :
```python
# models.py
class Review(models.Model):
    hotel = models.ForeignKey('hotels.Hotel', ...)
    user = models.ForeignKey('users.User', ...)
    # ... champs d'avis
```

**Avantages** :
- Séparation de la logique d'évaluation
- Possibilité de modération indépendante
- Calculs de ratings optimisés

### 6. Application `analytics` (Analyse de données)
**Responsabilités** :
- Statistiques d'utilisation
- Tableaux de bord personnalisés
- Tracking du comportement utilisateur

**Contenu** (à développer) :
```python
# models.py
class UserActivity(models.Model):
    user = models.ForeignKey('users.User', ...)
    # ... données de tracking

class HotelAnalytics(models.Model):
    hotel = models.ForeignKey('hotels.Hotel', ...)
    # ... statistiques métier
```

**Avantages** :
- Données d'analyse isolées
- Calculs performants
- Intégration facile avec des outils externes

### Structure finale recommandée :
```
project/
├── users/
├── hotels/
├── search/
├── bookings/
├── reviews/
└── analytics/
```

### Migration progressive étape par étape :

1. **Créer les nouvelles applications** :
```bash
python manage.py startapp users
python manage.py startapp hotels
python manage.py startapp search
```

2. **Déplacer les modèles** :
- Déplacer `User` et `HotelOwner` vers `users/models.py`
- Déplacer `Hotel` et `Room` vers `hotels/models.py`

3. **Mettre à jour les imports** :
```python
# Dans hotels/models.py
from users.models import HotelOwner

# Dans les vues et serializers
from users.models import User
from hotels.models import Hotel, Room
```

4. **Mettre à jour les paramètres** :
```python
# settings.py
INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'hotels.apps.HotelsConfig',
    'search.apps.SearchConfig',
    # ... autres apps
]

AUTH_USER_MODEL = 'users.User'
```

5. **Recréer les migrations** :
```bash
rm -rf */migrations/
python manage.py makemigrations users
python manage.py makemigrations hotels
python manage.py migrate
```

### Points de contrôle critiques :
1. Vérifier les relations entre modèles
2. Tester toutes les API existantes
3. Valider les permissions personnalisées
4. Vérifier le bon fonctionnement de l'admin

### Avantages de cette structure :
- **Maintenabilité** : Chaque fonctionnalité est isolée
- **Évolutivité** : Possibilité de déployer des apps séparément
- **Testabilité** : Tests plus ciblés et rapides
- **Réutilisation** : Composants génériques réutilisables

Cette décomposition préserve toutes vos fonctionnalités existantes tout en offrant une base solide pour les développements futurs.