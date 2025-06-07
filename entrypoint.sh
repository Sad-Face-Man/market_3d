#!/bin/sh

echo "Применение миграций..."
python manage.py migrate --noinput

echo "Запуск Gunicorn"
exec gunicorn --bind 0.0.0.0:8000 market_3d.wsgi:application
