import logging
import os
import uuid

from django.conf import settings
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)


def save_file_to_disk(uploaded_file, owner):
    """
    Сохраняет загруженный файл на диск.
    Возвращает кортеж (stored_name, file_path, size).
    """
    original_name = uploaded_file.name
    _, ext = os.path.splitext(original_name)
    stored_name = f"{uuid.uuid4().hex}{ext}"
    
    # Формируем путь внутри хранилища
    relative_path = f"{owner.storage_path}{stored_name}"
    full_path = os.path.join(settings.CLOUD_STORAGE_DIR, relative_path)
    
    # Создаём директорию, если её нет
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Сохраняем файл по частям (для больших файлов)
    size = 0
    try:
        with open(full_path, "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
                size += len(chunk)
        logger.info(f"Файл сохранён на диск: {full_path} ({size} байт)")
    except Exception as e:
        logger.error(f"Ошибка сохранения файла {full_path}: {e}")
        raise
        
    return stored_name, relative_path, size


def delete_file_from_disk(file_path):
    """
    Удаляет физический файл с диска.
    """
    full_path = os.path.join(settings.CLOUD_STORAGE_DIR, file_path)
    if os.path.exists(full_path):
        try:
            os.remove(full_path)
            logger.info(f"Файл удалён с диска: {full_path}")
        except OSError as e:
            logger.error(f"Ошибка удаления файла {full_path}: {e}")