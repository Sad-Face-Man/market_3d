import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Model3D
from utils.conversion import convert_to_glb
from market_3d.settings import MODEL_CONVERTED_ROOT  # <-- Используем твой путь


@receiver(post_save, sender=Model3D)
def convert_model_to_glb(sender, instance, created, **kwargs):
    if not created:
        return

    original_path = instance.file.path
    base_name = os.path.splitext(os.path.basename(original_path))[0]
    output_path = os.path.join(MODEL_CONVERTED_ROOT, f"{base_name}.glb")

    success = convert_to_glb(original_path, output_path)
    if success:
        print(f"[✓] Успешно конвертировано: {output_path}")
    else:
        print(f"[×] Ошибка при конвертации файла {original_path}")
