from django.db import models

from django.conf import settings  # Импортируем settings для AUTH_USER_MODEL
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from market_3d.constants import FileTypes

# Импорт переменных
from market_3d.settings import preview_storage,\
                                model3d_storage


class ModelTag(models.Model):
    """Теги для 3D моделей"""
    title = models.CharField(max_length=50, unique=True,
                            verbose_name="Название тега")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["title"]


class ModelLicense(models.Model):
    """Типы лицензий"""
    license_type = models.CharField(max_length=50, unique=True,
                                    verbose_name="Тип лицензии")

    def __str__(self):
        return self.license_type

    class Meta:
        verbose_name = "Лицензия"
        verbose_name_plural = "Лицензии"
        ordering = ["license_type"]


class Model3D(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=3000)

    # ----------- Временные метки -----------
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # ----------- Файловые характеристики -----------
    file_type = models.CharField(
        max_length=10,
        choices=FileTypes.CHOICES,
    )
    file_size = models.PositiveIntegerField(
        verbose_name="Размер файла (в байтах)")
    file = models.FileField(
        upload_to='3d_models/%Y/%m/%d/',
        storage=model3d_storage,
        validators=[FileExtensionValidator(allowed_extensions=FileTypes.EXTENSIONS)],
        verbose_name="Файл 3D-модели"
    )

    # ----------- Характеристики модели -----------
    animated = models.BooleanField(default=False,
                                   verbose_name="Анимированная модель.")

    # ----------- Публикация - покупка - скачивание -----------
    price = models.PositiveIntegerField(
        default=0,
        null=False,
        blank=True,
        verbose_name="Цена в долларах США",
    )
    download_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество скачиваний"
    )
    is_published = models.BooleanField(default=True,
                                       verbose_name="Опубликовано")


    # ----------- NFT -----------
    nft_token = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        verbose_name="NFT-токен (опционально)"
    )

    # -------------- Связи --------------
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='model3d',
                               verbose_name='Автор')

    tags = models.ManyToManyField(ModelTag, blank=True,
                                  related_name="models",
                                  verbose_name="Теги")

    license = models.ForeignKey('ModelLicense',
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name="models",
                                verbose_name="Тип лицензии")


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "3D модель"
        verbose_name_plural = "3D модели"
        ordering = ['-created_at']  # Сортировка по умолчанию
        indexes = [
            models.Index(fields=["-created_at"], name="idx_created_at_desc"),
            models.Index(fields=["author"], name="idx_author"),
            models.Index(fields=["title"], name="idx_title"),
        ]


class ModelImage(models.Model):
    model = models.ForeignKey('Model3D',
                              on_delete=models.CASCADE,
                              related_name='images',
                              verbose_name='3D-модель')
    image = models.ImageField(
        storage=preview_storage,    # from settings
        upload_to='model_images/%Y/%m/%d/',
        verbose_name='Изображение превью'
    )

    def __str__(self):
        return f'Изображение для {self.model.title}'

    class Meta:
        verbose_name = 'Изображение модели'
        verbose_name_plural = 'Изображения моделей'