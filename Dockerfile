# Используйте официальный образ Python 3.9
FROM python:3.9-slim

# Установка рабочей директории
WORKDIR /app

# Копирование файла с зависимостями
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование скрипта и файлов .env
COPY dto.py .
COPY messages.py .
COPY services.py .
COPY bot.py .
COPY utils.py .
COPY .env .

# Запуск скрипта
CMD ["python", "bot.py"]