import os
import shutil
import logging

from django.core.files import File
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Model3D
from utils.conversion import convert_to_glb
from market_3d import settings
from market_3d.settings import MODEL_CONVERTED_ROOT

from market_3d.constants import FileTypes

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Model3D)
def convert_model_to_glb(sender, instance, created, **kwargs):
    if not created:
        return

    original_path = instance.file.path

    # Проверка допустимого расширения
    allowed_exts = tuple(f".{ext}" for ext in FileTypes.EXTENSIONS if ext != 'glb')
    if not original_path.lower().endswith(allowed_exts):
        logger.warning(f"[!] Неподдерживаемое расширение файла: {original_path}")
        return

    base_name = os.path.splitext(os.path.basename(original_path))[0]
    output_path = os.path.join(MODEL_CONVERTED_ROOT, f"{base_name}.glb")

    success = convert_to_glb(original_path, output_path)
    if success:
        logger.info(f"[✓] Успешно конвертировано: {output_path}")
        with open(output_path, 'rb') as f:
            instance.converted_file.save(f"{base_name}.glb", File(f), save=True)
    else:
        logger.error(f"[×] Ошибка при конвертации файла {original_path}")


@receiver(post_delete, sender=Model3D)
def delete_model3d_files(sender, instance, **kwargs):
    base_dir = os.path.join("3d_models", f"model_{instance.uuid}")
    full_path = os.path.join(settings.MEDIA_ROOT, base_dir)
    if os.path.exists(full_path):
        shutil.rmtree(full_path)
        logger.info(f"[🗑] Удалена директория модели: {full_path}")
    else:
        logger.warning(f"[!] Папка для удаления не найдена: {full_path}")
