FROM python:3.13-slim

WORKDIR /app

# Сначала копируем только requirements.txt для кэширования
COPY ./requirements.txt ./requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Затем копируем ВСЕ содержимое проекта
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]