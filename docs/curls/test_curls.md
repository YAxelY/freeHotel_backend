# Enregistrement utilisateur
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123", "username": "testuser"}'

# Login et récupération du token (à stocker)
TOKEN=$(curl -X POST http://localhost:8000/api/auth/token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username_or_email": "user@example.com", "password": "password123"}' | jq -r '.token')

echo "Token stored in \$TOKEN: $TOKEN"

# Création d'un hôtel (propriétaire)
curl -X POST http://localhost:8000/api/hotels/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Grand Hotel", "location": "Paris", "description": "Hôtel luxueux"}'

# Recherche d'hôtels
curl -X GET "http://localhost:8000/api/search/hotels/?q=paris" \
  -H "Authorization: Token $TOKEN"

# Création d'une réservation
curl -X POST http://localhost:8000/api/reservations/create/ \
  -H "Authorization: Token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"room": 1, "check_in": "2024-01-15", "check_out": "2024-01-20"}'