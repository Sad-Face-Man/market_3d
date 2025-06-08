import django_filters
from django_filters import rest_framework as filters
from .models import Model3D


class Model3DFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    file_type = filters.CharFilter(lookup_expr='iexact')
    file_size_min = filters.NumberFilter(field_name='file_size', lookup_expr='gte')
    file_size_max = filters.NumberFilter(field_name='file_size', lookup_expr='lte')
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    download_count_min = filters.NumberFilter(field_name='download_count', lookup_expr='gte')
    download_count_max = filters.NumberFilter(field_name='download_count', lookup_expr='lte')
    is_published = filters.BooleanFilter()
    animated = filters.BooleanFilter()
    nft_token = filters.CharFilter(lookup_expr='exact')
    author = filters.NumberFilter(field_name='author__id')
    author_username = filters.CharFilter(field_name='author__username', lookup_expr='icontains')
    license = filters.NumberFilter(field_name='license__id')
    license_name = filters.CharFilter(field_name='license__license_type', lookup_expr='icontains')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_after = filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_before = filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__id',
        to_field_name='id',
        queryset=Model3D._meta.get_field('tags').related_model.objects.all()
    )

    class Meta:
        model = Model3D
        fields = []  # Все поля указаны вручную
