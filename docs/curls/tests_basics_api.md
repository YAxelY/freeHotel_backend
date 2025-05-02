Voici la liste complète des API et fonctionnalités implémentées, avec des exemples de tests cURL utilisant des variables d'environnement pour le token :

### Tableau des Endpoints API

| Méthode | Endpoint | Description | Permissions Requises |
|---------|----------|-------------|----------------------|
| POST | `/api/auth/register/` | Création d'utilisateur standard | Aucune |
| POST | `/api/auth/register/hotel-owner/` | Création de profil propriétaire d'hôtel | Utilisateur authentifié |
| POST | `/api/auth/login/` | Connexion et obtention de token | Aucune |
| POST | `/api/auth/logout/` | Déconnexion et suppression du token | Utilisateur authentifié |
| GET | `/api/auth/me/` | Récupération du profil utilisateur | Utilisateur authentifié |
| POST | `/api/auth/token-auth/` | Obtention de token (alternative) | Aucune |
| GET | `/api/hotels/` | Liste des hôtels | Lecture publique |
| POST | `/api/hotels/` | Création d'hôtel | Propriétaire d'hôtel |
| GET | `/api/hotels/<id>/` | Détails d'un hôtel | Lecture publique |
| GET | `/api/hotels/<id>/rooms/` | Liste des chambres d'un hôtel | Propriétaire d'hôtel |
| POST | `/api/hotels/<id>/rooms/` | Création de chambre | Propriétaire d'hôtel |
| GET | `/api/search/hotels/` | Recherche d'hôtels | Lecture publique |

### Tests cURL avec gestion de token

1. **Configuration initiale**
```bash
# Stocker l'URL de base
export API_URL="http://localhost:8000"
```

2. **Enregistrement utilisateur**
```bash
curl -X POST $API_URL/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!",
    "username": "testuser"
  }'
```

3. **Connexion et récupération du token**
```bash
RESPONSE=$(curl -s -X POST $API_URL/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "test3@example.com",
    "password": "Test3Pass123!"
  }')

export TOKEN=$(echo $RESPONSE | jq -r '.token')
export USER_ID=$(echo $RESPONSE | jq -r '.user.id')
```

4. **Enregistrement comme propriétaire d'hôtel**
```bash
curl -X POST $API_URL/api/auth/register/hotel-owner/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d '{
    "business_name": "Mon Hôtel",
    "contact_number": "+123456789"
  }'
```

5. **Création d'un hôtel**
```bash
curl -X POST $API_URL/api/hotels/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d '{
    "name": "Grand Hôtel",
    "location": "Paris",
    "description": "Un hôtel de luxe",
    "amenities": ["piscine", "spa"]
  }'
```

6. **Liste des hôtels (public)**
```bash
curl -X GET $API_URL/api/hotels/
```

7. **Création d'une chambre**
```bash
curl -X POST $API_URL/api/hotels/1/rooms/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d '{
    "room_number": "101",
    "room_type": "Deluxe",
    "price_per_night": 299.99,
    "capacity": 2
  }'
```

8. **Récupération du profil utilisateur**
```bash
curl -X GET $API_URL/api/auth/me/ \
  -H "Authorization: Token $TOKEN"
```

9. **Recherche d'hôtels**
```bash
curl -X GET "$API_URL/api/search/hotels/?q=paris"
```

10. **Déconnexion**
```bash
curl -X POST $API_URL/api/auth/logout/ \
  -H "Authorization: Token $TOKEN"
```

### Workflow complet exemple
```bash
# 1. Création utilisateur
curl -X POST $API_URL/api/auth/register/ -H "Content-Type: application/json" -d '{"email":"user@test.com","password":"Pass123!","username":"testuser"}'

# 2. Connexion
RESPONSE=$(curl -s -X POST $API_URL/api/auth/login/ -H "Content-Type: application/json" -d '{"username_or_email":"user@test.com","password":"Pass123!"}')
export TOKEN=$(echo $RESPONSE | jq -r '.token')

# 3. Création profil propriétaire
curl -X POST $API_URL/api/auth/register/hotel-owner/ -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" -d '{"business_name":"My Hotel","contact_number":"+111111111"}'

# 4. Création hôtel
curl -X POST $API_URL/api/hotels/ -H "Authorization: Token $TOKEN" -H "Content-Type: application/json" -d '{"name":"Beach Resort","location":"Miami","description":"Super hôtel"}'

# 5. Liste des hôtels
curl -X GET $API_URL/api/hotels/ -H "Authorization: Token $TOKEN"
```

### Gestion des erreurs courantes
- **401 Unauthorized** : Vérifier le token et les permissions
- **403 Forbidden** : Vérifier le statut de propriétaire d'hôtel
- **400 Bad Request** : Vérifier le format des données envoyées

Vous pouvez utiliser des outils comme [jq](https://stedolan.github.io/jq/) pour parser les réponses JSON directement dans le terminal.