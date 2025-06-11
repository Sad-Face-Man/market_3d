# ------------------------- Blender Layer -------------------------
# Данный слой может не пересобираться каждый раз, при билде
# Blender Ставится отдельным C++ приложением с зависимостями, потому что
# его аналог-библиотека на Python:
# неофициальная, неактуальная и весит очень много.

FROM blender-runtime AS blender

# ------------------------- Builder Layer -------------------------
FROM python:3.13-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput


# ------------------------- Final Runtime Layer -------------------------
FROM python:3.13-slim

WORKDIR /app

# Установка библиотек, необходимых для Blender и PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libgl1 libx11-6 libxkbcommon0 \
    libxrender1 libxrandr2 libxfixes3 libxi6 \
    libxcursor1 libxcomposite1 libasound2 \
    libxdamage1 libxext6 libsm6 libxxf86vm1 \
    && rm -rf /var/lib/apt/lists/*

# Копируем Blender из отдельного слоя
COPY --from=blender /opt/blender /opt/blender
COPY --from=blender /usr/local/bin/blender /usr/local/bin/blender
ENV PATH="/opt/blender:$PATH"

# Копируем собранный Python-проект и зависимости
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Переменные окружения Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Порт для приложения
EXPOSE 8000

# Команда запуска Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "market_3d.wsgi:application"]
