import os
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Model3D, ModelTag, ModelImage
from .serializers import Model3DSerializer, TagSerializer, ModelImageSerializer
from .filters import Model3DFilter
from .permissions import IsAuthorOrReadOnly
from market_3d.constants import FileTypes

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Model3DViewSet(viewsets.ModelViewSet):
    queryset = Model3D.objects.all().select_related('author', 'license').prefetch_related('tags')
    serializer_class = Model3DSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_class = Model3DFilter
    search_fields = ['title', 'description', 'nft_token']
    ordering_fields = ['created_at', 'price', 'download_count', 'file_size']

    @swagger_auto_schema(  # <-- Только один декоратор для create
        operation_description="Загрузка новой 3D модели",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'file', 'file_type', 'file_size'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Название модели'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Описание'),
                'file': openapi.Schema(type=openapi.TYPE_FILE, description='Файл 3D модели (.fbx, .obj и др.)'),
                'file_type': openapi.Schema(type=openapi.TYPE_STRING, description='Тип файла (FBX/OBJ/BLEND/GLB)'),
                'file_size': openapi.Schema(type=openapi.TYPE_INTEGER, description='Размер файла в байтах'),
                'price': openapi.Schema(type=openapi.TYPE_INTEGER, description='Цена (в долларах)'),
                'nft_token': openapi.Schema(type=openapi.TYPE_STRING, description='NFT-токен'),
                'tags': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description='Список ID тегов'
                ),
                'is_published': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Опубликовано'),
            }
        )
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(  # <-- отдельный декоратор для list
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, description="Название (поиск по подстроке)", type=openapi.TYPE_STRING),
            openapi.Parameter('description', openapi.IN_QUERY, description="Описание (поиск по подстроке)", type=openapi.TYPE_STRING),
            openapi.Parameter('file_type', openapi.IN_QUERY, description="Тип файла (FBX, OBJ, GLB...)", type=openapi.TYPE_STRING),
            openapi.Parameter('animated', openapi.IN_QUERY, description="Анимированная модель (true/false)", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('price_min', openapi.IN_QUERY, description="Цена от", type=openapi.TYPE_INTEGER),
            openapi.Parameter('price_max', openapi.IN_QUERY, description="Цена до", type=openapi.TYPE_INTEGER),
            openapi.Parameter('tags', openapi.IN_QUERY, description="ID тега (можно несколько)", type=openapi.TYPE_INTEGER, collection_format='multi'),
            openapi.Parameter('author', openapi.IN_QUERY, description="ID автора", type=openapi.TYPE_INTEGER),
            openapi.Parameter('created_after', openapi.IN_QUERY, description="Создано после (YYYY-MM-DD)", type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('created_before', openapi.IN_QUERY, description="Создано до (YYYY-MM-DD)", type=openapi.TYPE_STRING, format='date'),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        file = self.request.FILES.get('file')
        file_type = self.guess_file_type(file.name) if file else None

        serializer.save(author=self.request.user, file_type=file_type)

    @staticmethod
    def guess_file_type(filename: str) -> str:
        ext = os.path.splitext(filename)[1].lower().strip(".")
        if ext in FileTypes.EXTENSIONS:
            # Найдём имя класса (например, 'OBJ'),
            # соответствующее этому расширению
            for key, value in FileTypes.__dict__.items():
                if not key.startswith("_") and isinstance(value,
                                                          str) and value.lower() == ext:
                    return value  # Вернёт 'OBJ', 'GLB' и т.д.
        return 'UNKNOWN'


class TagViewSet(viewsets.ModelViewSet):
    queryset = ModelTag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ModelImageViewSet(viewsets.ModelViewSet):
    queryset = ModelImage.objects.all()
    serializer_class = ModelImageSerializer
    permission_classes = [permissions.IsAuthenticated]
