import bpy
import sys

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # Blender передаёт аргументы после --

input_file = argv[0]
output_file = argv[1]

# Очистить сцену
bpy.ops.wm.read_factory_settings(use_empty=True)

# Импорт по расширению
if input_file.lower().endswith(".fbx"):
    bpy.ops.import_scene.fbx(filepath=input_file)
elif input_file.lower().endswith(".obj"):
    bpy.ops.import_scene.obj(filepath=input_file)
elif input_file.lower().endswith(".blend"):
    bpy.ops.wm.open_mainfile(filepath=input_file)
else:
    raise Exception("Unsupported input format")

# Экспорт в .glb
bpy.ops.export_scene.gltf(filepath=output_file, export_format='GLB')
