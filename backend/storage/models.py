import uuid
from django.conf import settings
from django.db import models

# Create your models here.
def generate_share_token():
    return uuid.uuid4()


class File(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="владелец",
    )
    file_name = models.CharField("имя файла", max_length=255)
    stored_name = models.CharField("имя на диске", max_length=64)
    size = models.BigIntegerField("размер, байт")
    uploaded_at = models.DateTimeField("дата загрузки", auto_now_add=True)
    last_downloaded_at = models.DateTimeField(
        "дата последнего скачивания",
        null=True,
        blank=True,
    )
    comment = models.CharField("комментарий", max_length=300, blank=True)
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

    def __str__(self):
        return self.file_name