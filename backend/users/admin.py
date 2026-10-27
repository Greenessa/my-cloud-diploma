
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Настройка отображения кастомной модели User в админке.
    Наследуемся от встроенного UserAdmin, чтобы сохранить
    удобные функции (смена пароля, фильтры по правам).
    """

    # Колонки в списке пользователей
    list_display = (
        "id",
        "username",
        "email",
        "full_name",
        "is_admin",
        "is_staff",
        "is_active",
        "storage_path",
    )

    # Фильтры справа
    list_filter = ("is_admin", "is_staff", "is_superuser", "is_active")

    # Поиск по этим полям
    search_fields = ("username", "email", "full_name")

    # Сортировка по умолчанию
    ordering = ("id",)

    # Поля, которые нельзя редактировать
    readonly_fields = ("last_login", "date_joined", "storage_path")

    # Группировка полей в форме редактирования
    fieldsets = (
        (None, {
            "fields": ("username", "password"),
        }),
        ("Персональные данные", {
            "fields": ("full_name", "email"),
        }),
        ("Права", {
            "fields": ("is_admin", "is_active", "is_staff", "is_superuser"),
        }),
        ("Хранилище", {
            "fields": ("storage_path",),
        }),
        ("Служебное", {
            "fields": ("last_login", "date_joined"),
        }),
    )

    # Поля для формы создания пользователя
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "full_name",
                "email",
                "password1",
                "password2",
                "is_admin",
            ),
        }),
    )