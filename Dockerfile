# ------------------------- Blender Layer -------------------------
# Данный слой может не пересобираться каждый раз, при билде
# Blender Ставится отдельным C++ приложением с зависимостями, потому что
# его аналог-библиотека на Python:
# неофициальная, неактуальная и весит очень много.

FROM python:3.13-slim as blender


ENV BLENDER_VERSION=3.6.12
# Добавление Blender в переменную среды
ENV PATH="/opt/blender:$PATH"

# # Установка зависимостей и X-библиотек для корректной работы Blender.
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget ca-certificates tar xz-utils && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /opt/blender && \
    wget -q https://download.blender.org/release/Blender${BLENDER_VERSION%.*}/blender-${BLENDER_VERSION}-linux-x64.tar.xz && \
    tar -xf blender-${BLENDER_VERSION}-linux-x64.tar.xz --strip-components=1 -C /opt/blender && \
    ln -s /opt/blender/blender /usr/local/bin/blender


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

# Установка библиотек, необходимых для работы Blender
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 libgl1 libxrender1 libxrandr2 libxfixes3 libxi6 libxcursor1 \
    libxcomposite1 libasound2 libxdamage1 libxext6 libx11-6 && \
    rm -rf /var/lib/apt/lists/*

# Копируем Blender из отдельного слоя
COPY --from=blender /opt/blender /opt/blender
COPY --from=blender /usr/local/bin/blender /usr/local/bin/blender
ENV PATH="/opt/blender:$PATH"

# Копируем собранный Python-проект
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
# Без этого не копируются собранные бинарники после установки зависимостей
# была проблема с gunicorn (бинарники не переносились в финальный образ)
COPY --from=builder /usr/local/bin /usr/local/bin

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "market_3d.wsgi:application"]
