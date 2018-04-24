del /Q db.sqlite3
python manage.py migrate
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'TuProfe1234')"
python manage.py runserver