from .base import *

# Режим продакшена: ошибки не показываем, статику отдаёт Nginx
DEBUG = False

# Читаем домены из .env (на сервере там будет твой домен)
# Если переменная не задана, разрешаем только сам сервер
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost").split(",")


# --- Настройки безопасности для HTTPS (включаются на сервере) ---
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Настройки CORS и CSRF для продакшена
# Читаем адреса из переменных окружения. Если не заданы — по умолчанию пустой список.
cors_origins_str = os.getenv("CORS_ALLOWED_ORIGINS", "")
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]

csrf_origins_str = os.getenv("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_origins_str.split(",") if origin.strip()]

# На продакшене обязательно разрешаем куки (для сессий)
CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}