import os
import logging
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import File

logger = logging.getLogger(__name__)

@receiver(post_delete, sender=File)
def delete_file_on_disk(sender, instance, **kwargs):
    """
    Удаляет физический файл с диска после удаления записи из БД.
    """
    if not instance.file_path:
        return

    # Формируем полный путь: CLOUD_STORAGE_DIR / file_path
    full_path = os.path.join(settings.CLOUD_STORAGE_DIR, instance.file_path)
    
    if os.path.exists(full_path):
        try:
            os.remove(full_path)
            logger.info(f"Файл удалён с диска: {full_path}")
        except OSError as e:
            logger.error(f"Ошибка при удалении файла {full_path}: {e}")
    else:
        logger.warning(f"Попытка удалить несуществующий файл: {full_path}")