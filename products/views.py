from rest_framework import viewsets, permissions
from .models import Model3D, ModelTag
from .serializers import Model3DSerializer, TagSerializer


class Model3DViewSet(viewsets.ModelViewSet):
    queryset = Model3D.objects.all().select_related('author').prefetch_related('tags')
    serializer_class = Model3DSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = ModelTag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
