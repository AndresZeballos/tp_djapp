del /Q db.sqlite3
python manage.py migrate
python manage.py loaddata db.json
python manage.py runserver