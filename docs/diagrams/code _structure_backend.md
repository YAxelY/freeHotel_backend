hotelSystem/
├── hotelSystem/        ← Dossier principal du projet (config globale)
│   ├── __init__.py
│   ├── settings.py     ← Paramètres (DB, apps installées, etc.)
│   ├── urls.py         ← URLs globales du projet
│   ├── asgi.py
│   └── wsgi.py
├── manage.py           ← Interface CLI de Django



myproject/                     # Racine du projet
├── .github/                   # Configuration CI/CD
│   └── workflows/
│       └── django-ci.yml
├── .gitignore
├── .env.example               # Template des variables d'environnement
├── .pre-commit-config.yaml    # Linters/formatters
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml             # Configuration Poetry
├── Makefile                   # Commandes utiles
├── README.md
│
├── backend/                   # Dossier principal Django
│   ├── apps/
│   │   ├── core/             # Fonctionnalités transverses
│   │   │   ├── migrations/
│   │   │   ├── models/
│   │   │   ├── api/
│   │   │   │   ├── v1/      # Versioning d'API
│   │   │   │   │   ├── serializers/
│   │   │   │   │   ├── views/
│   │   │   │   │   └── routers.py
│   │   │   ├── services/
│   │   │   ├── utils/
│   │   │   ├── tests/
│   │   │   └── __init__.py
│   │   │
│   │   ├── hotels/           # App spécifique (ex: gestion hôtelière)
│   │   │   └── (même structure que core)
│   │   └── users/            # Gestion utilisateurs
│   │
│   ├── config/               # Configuration du projet
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py       # Config commune
│   │   │   ├── local.py      # Développement
│   │   │   └── production.py # Production
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── static/               # Fichiers statiques
│   │   └── sass/            # Sources SCSS
│   ├── media/                # Fichiers uploadés
│   ├── templates/            # Templates globaux
│   └── requirements/
│       ├── base.txt          # Dépendances communes
│       ├── dev.txt           # Développement
│       └── prod.txt          # Production
│
├── docs/                     # Documentation technique
│   ├── architecture.md
│   └── api-spec.yaml         # OpenAPI Specification
│
└── scripts/                  # Scripts utilitaires
    ├── deploy.sh
    └── setup_db.sh