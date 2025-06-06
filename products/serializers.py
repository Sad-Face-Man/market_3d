from rest_framework import serializers
from .models import ModelTag, Model3D


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTag
        fields = ['id', 'title']


class Model3DSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Model3D
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'updated_at',
            'file_type',
            'file_size',
            'file',
            'price',
            'download_count',
            'is_published',
            'author',
            'author_username',
            'tags'
        ]
        read_only_fields = ['download_count', 'created_at', 'updated_at', 'author']
