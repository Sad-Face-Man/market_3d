class FileTypes:
    """Доступные расширения файлов 3D моделей"""
    OBJ = 'OBJ'
    STL = 'STL'
    FBX = 'FBX'
    BLEND = 'BLEND'
    GLTF = 'GLTF'

    CHOICES = [
        (OBJ, 'Wavefront OBJ'),
        (STL, 'Stereolithography'),
        (FBX, 'Autodesk FBX'),
        (BLEND, 'Blender'),
        (GLTF, 'GL Transmission Format'),
    ]

    EXTENSIONS = [OBJ.lower(), STL.lower(), FBX.lower(), BLEND.lower(),
                  GLTF.lower()]