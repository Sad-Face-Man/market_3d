import subprocess
import os
from django.conf import settings


def convert_to_glb(input_path: str, output_path: str) -> bool:
    try:
        subprocess.run([
            "blender", "--background", "--python", os.path.join(settings.BASE_DIR, "scripts/convert_to_glb.py"),
            "--", input_path, output_path
        ], check=True)
        return os.path.exists(output_path)
    except subprocess.CalledProcessError as e:
        print(f"Conversion error: {e}")
        return False
