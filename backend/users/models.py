from django.contrib.auth.models import AbstractUser
from django.db import models

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
        # Автозаполнение storage_path при первом сохранении.
        if not self.storage_path and self.pk is None:
            super().save(*args, **kwargs)
            self.storage_path = f"user_{self.pk}/"
            return super().save(update_fields=["storage_path"])
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username

