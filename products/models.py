from django.db import models

from django.conf import settings  # Импортируем settings для AUTH_USER_MODEL
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from market_3d.constants import FileTypes

class Tag(models.Model):
    """Модель тегов для 3D моделей на сайте"""
    title = models.CharField(max_length=50, unique=True,
                            verbose_name="Название тега")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["title"]

class Model3D(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=3000)

    # Временные метки
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Файловые характеристики
    file_type = models.CharField(
        max_length=10,
        choices=FileTypes.CHOICES,
    )
    file_size = models.PositiveIntegerField(
        verbose_name="Размер файла (в байтах)")
    file = models.FileField(
        upload_to='3d_models/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=FileTypes.EXTENSIONS)],
        verbose_name="Файл 3D-модели"
    )

    # Дополнительные поля
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена в рублях",
        null=True,
        blank=True
    )
    download_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество скачиваний"
    )
    is_published = models.BooleanField(default=True,
                                       verbose_name="Опубликовано")

    # Связи
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='model3d',
                               verbose_name='Автор')
    tags = models.ManyToManyField(Tag, blank=True,
                                  related_name="models",
                                  verbose_name="Теги")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "3D модель"
        verbose_name = "3D модели"
        ordering = ['-created_at']  # Сортировка по умолчанию
        indexes = [
            models.Index(fields=["-created_at"], name="idx_created_at_desc"),
            models.Index(fields=["author"], name="idx_author"),
            models.Index(fields=["title"], name="idx_title"),
        ]
