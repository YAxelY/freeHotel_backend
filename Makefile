# Makefile

.PHONY: updateRequirements

updateRequirements:
	@echo "🔧 Generating requirements.txt…"
	pip freeze > requirements.txt
	@echo "✅ requirements.txt updated"

full-migrate:
	python manage.py makemigrations users
	python manage.py makemigrations hotels
	python manage.py makemigrations
	python manage.py migrate

migrate:
	python manage.py makemigrations
	python manage.py migrate

install:

	pip install django djangorestframework django-cors-headers psycopg2-binary python-dotenv django_filter

run:
	python manage.py runserver

test:
	python manage.py test hotels
	python manage.py test users
	python manage.py test search