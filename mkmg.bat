@echo off



python manage.py makemigrations
python manage.py migrate
cls
python manage.py runserver

