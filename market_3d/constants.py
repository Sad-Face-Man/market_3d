class FileTypes:
    """Доступные расширения файлов 3D моделей"""
    OBJ = 'OBJ'
    GLB = 'GLB'
    FBX = 'FBX'
    BLEND = 'BLEND'

    CHOICES = [
        (OBJ, 'Wavefront OBJ'),
        (GLB, 'GL Transmission Format Binary file'),
        (FBX, 'Autodesk FBX'),
        (BLEND, 'Blender'),
    ]

    EXTENSIONS = [OBJ.lower(), GLB.lower(), FBX.lower(), BLEND.lower()]