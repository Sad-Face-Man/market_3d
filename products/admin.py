from django.contrib import admin
from .models import Model3D, ModelTag, ModelLicense, ModelImage


class ModelImageInline(admin.TabularInline):
    model = ModelImage
    extra = 1
    fields = ('image', 'is_main', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" style="object-fit: contain;" />'
        return "-"
    image_preview.allow_tags = True
    image_preview.short_description = "Превью"


@admin.register(Model3D)
class Model3DAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'file_type', 'animated', 'created_at', 'is_published')
    list_filter = ('file_type', 'is_published', 'created_at', 'animated')
    search_fields = ('title', 'description')
    inlines = [ModelImageInline]
    autocomplete_fields = ['tags', 'license']
    list_select_related = ('license', 'author')
    date_hierarchy = 'created_at'


@admin.register(ModelTag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(ModelLicense)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('license_type',)
    search_fields = ('license_type',)
