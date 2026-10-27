import os
import uuid
from django.conf import settings
from django.db import models

# Create your models here.
def generate_share_token():
    return uuid.uuid4()


class File(models.Model):
    """
    Модель файла в облачном хранилище.
    
    stored_name формируется как UUID4 в формате hex с расширением файла:
    f"{uuid.uuid4().hex}{ext}" (например, "a1b2c3d4...ef.pdf").
    Длина в 64 символа покрывает UUID (32 символа в hex) и до 32 символов расширения.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="владелец",
    )
    # Оригинальное имя файла, введенное пользователем. 
    # Используется ТОЛЬКО для отображения в интерфейсе и при скачивании.
    # НИКОГДА не используется для формирования пути на диске.
    file_name = models.CharField("имя файла", max_length=255)
    # Имя файла на диске. Генерируется ТОЛЬКО на сервере (UUID4 + расширение).
    # Никогда не берется из пользовательского ввода — это защита от path traversal.
    stored_name = models.CharField(
        "имя на диске", 
        max_length=64,
        help_text="Формат: UUID4 hex + расширение файла (например, 'a1b2c3d4...ef.pdf')"
    )
    size = models.BigIntegerField("размер, байт")
    uploaded_at = models.DateTimeField("дата загрузки", auto_now_add=True)
    last_downloaded_at = models.DateTimeField(
        "дата последнего скачивания",
        null=True,
        blank=True,
    )
    comment = models.TextField("комментарий", blank=True)
    # Относительный путь к файлу внутри CLOUD_STORAGE_DIR (а не MEDIA_ROOT!)
    # Формируется автоматически в методе save() как f"{owner.storage_path}{stored_name}".
    # Так как stored_name — это UUID, path traversal исключен.
    file_path = models.CharField("путь к файлу", max_length=512)
    share_token = models.UUIDField(
        "токен публичной ссылки",
        default=generate_share_token,
        unique=True,
        editable=False,
    )

    class Meta:
        verbose_name = "файл"
        verbose_name_plural = "файлы"
        ordering = ["-uploaded_at"]
        indexes = [
            models.Index(fields=["-uploaded_at"], name="file_uploaded_at_idx"),
        ]

    def __str__(self):
        return self.file_name
    
    def save(self, *args, **kwargs):
        # Автозаполнение file_path при первом сохранении
        if not self.file_path and self.owner:
            # 1. Отделяем расширение от имени файла (например, ".pdf")
            _, ext = os.path.splitext(self.file_name)
            
            # 2. Если stored_name ещё не задан, генерируем его на основе UUID
            # (по нашему плану это должно делаться во вьюхе, но для надёжности добавим и здесь)
            if not self.stored_name:
                self.stored_name = f"{uuid.uuid4().hex}{ext}"
                
            # 3. Формируем полный путь: storage_path пользователя + имя на диске
            # У пользователя storage_path имеет вид "user_xxxx/" (со слешем в конце)
            self.file_path = f"{self.owner.storage_path}{self.stored_name}"
            
        super().save(*args, **kwargs)