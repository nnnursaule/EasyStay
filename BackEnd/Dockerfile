# Базовый образ Python
FROM python:3.11-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё остальное
COPY . /app/

# Делаем entrypoint исполняемым
RUN chmod +x /app/entrypoint.sh

# Настройки Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Точка входа
ENTRYPOINT ["/app/entrypoint.sh"]
