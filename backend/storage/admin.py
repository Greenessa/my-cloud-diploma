
# Register your models here.
from django.contrib import admin

from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    """
    Настройка отображения модели File в админке.
    """

    # Колонки в списке файлов
    list_display = (
        "id",
        "file_name",
        "owner",
        "size",
        "uploaded_at",
        "last_downloaded_at",
        "short_share_token",
    )

    # Фильтры справа
    list_filter = ("uploaded_at", "owner")

    # Поиск
    search_fields = ("file_name", "comment", "owner__username")

    # Сортировка
    ordering = ("-uploaded_at",)

    # Поля, недоступные для редактирования
    readonly_fields = (
        "stored_name",
        "file_path",
        "share_token",
        "uploaded_at",
        "last_downloaded_at",
    )

    # Группировка полей
    fieldsets = (
        ("Основное", {
            "fields": ("owner", "file_name", "comment"),
        }),
        ("Файл", {
            "fields": ("stored_name", "file_path", "size"),
        }),
        ("Публичный доступ", {
            "fields": ("share_token",),
        }),
        ("Служебное", {
            "fields": ("uploaded_at", "last_downloaded_at"),
        }),
    )

    # Удобное отображение токена (обрезанное)
    @admin.display(description="Токен")
    def short_share_token(self, obj):
        return str(obj.share_token)[:8] + "…"