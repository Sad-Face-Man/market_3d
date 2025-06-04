from django.db import models
# Расширение функционала
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Стандартные поля уже включены в AbstractUser
    # username(логин),
    # email,
    # first_name, last_name,
    # date_joined,
    # is_active, is_staff, is_superuser и др.


    # изменение обычных полей
    email = models.EmailField(unique=True, verbose_name="Email")

    # Дополнительные поля
    avatar = models.ImageField(upload_to='avatar/',
                               blank=True, null=True,
                               verbose_name='Аватар')
    phone = models.CharField(max_length=20, blank=True, null=True,
                             verbose_name="Номер телефона")
    bio = models.TextField(blank=True,
                           verbose_name="Информация \"о себе\"")


    def __str__(self):
        return self.username


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = [
            '-date_joined']  # Сортировка по дате регистрации (новые сначала)
        indexes = [
            models.Index(fields=['username'], name='idx_user_username'),
            models.Index(fields=['email'], name='idx_user_email'),
        ]
