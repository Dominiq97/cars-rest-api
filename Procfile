release: python manage.py majemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn app.wsgi