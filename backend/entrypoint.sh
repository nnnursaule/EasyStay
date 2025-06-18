#!/bin/sh

echo "🕒 Ожидание PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "✅ PostgreSQL доступен."

# Загружаем переменные окружения
echo "📦 Применение миграций..."
python manage.py migrate

echo "📦 Сбор статических файлов..."
python manage.py collectstatic --noinput

echo "🚀 Запуск сервера..."
exec python manage.py runserver 0.0.0.0:8000
