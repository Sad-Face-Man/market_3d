from rest_framework import viewsets, permissions
from .models import Model3D, ModelTag
from .serializers import Model3DSerializer, TagSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsAuthorOrReadOnly


class Model3DViewSet(viewsets.ModelViewSet):
    queryset = Model3D.objects.all().select_related('author').prefetch_related('tags')
    serializer_class = Model3DSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['tags', 'file_type', 'is_published']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price', 'download_count']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = ModelTag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
