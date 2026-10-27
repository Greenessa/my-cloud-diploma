from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

from .managers import UserManager
from .validators import validate_password_strength, validate_username

# Create your models here.

class User(AbstractUser):
    """
    Кастомная модель пользователя.
    Расширяет AbstractUser (берём username, email, password,
    is_staff, is_superuser) и добавляет поля из ТЗ.
    """

    # Убираем first_name/last_name, они не нужны — есть full_name.
    first_name = None
    last_name = None

    username = models.CharField(
        "логин",
        max_length=20,
        unique=True,
        validators=[validate_username],
    )
    full_name = models.CharField("полное имя", max_length=255)
    email = models.EmailField("email", unique=True)
    is_admin = models.BooleanField("администратор", default=False)
    storage_path = models.CharField(
        "путь к хранилищу",
        max_length=255,
        unique=True, 
        blank=True,
        default="",
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "full_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["id"]

    
    def save(self, *args, **kwargs):
        # Если это новый пользователь (ещё нет ID в базе) и путь не задан,
        # генерируем уникальное имя папки на основе UUID.
        if not self.storage_path and self.pk is None:
            self.storage_path = f"user_{uuid.uuid4().hex}/"
        
        # Вызываем сохранение ОДИН раз. 
        # Django сам сохранит и данные пользователя, и сгенерированный storage_path.
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """
        Возвращает полное имя пользователя.
        Переопределяем метод из AbstractUser, так как мы убрали
        поля first_name и last_name.
        """
        return self.full_name

    def get_short_name(self):
        """
        Возвращает короткое имя (обычно используется для обращения).
        Возвращаем логин.
        """
        return self.username

