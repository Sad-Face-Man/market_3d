# Генерация путей сохранения моделей и изображений на сервер
import os
from uuid import uuid4
import logging


logger = logging.getLogger(__name__)  # Получаем логгер для текущего модуля


def get_model_directory(instance, filename):
    """
    Путь для оригинального файла модели.
    """
    if not instance.uuid:
        instance.uuid = uuid4()
    path = os.path.join("3d_models", f"model_{instance.uuid}", "original",
                        filename)
    logger.debug(f"[UPLOAD PATH] {path}")

    return path

def get_converted_model_path(instance, filename):
    """
    Путь для конвертированного файла модели (.glb).
    """
    return os.path.join("3d_models", f"model_{instance.uuid}", "converted", filename)


def get_preview_image_path(instance, filename):
    """
    Путь для изображения-превью.
    """
    return os.path.join("3d_models", f"model_{instance.model.uuid}", "preview", filename)
