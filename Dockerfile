# Базовый образ Python
FROM python:3.11

# Установка рабочей директории
WORKDIR /Medicine_service

# Копирование файла зависимостей
COPY . .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt




