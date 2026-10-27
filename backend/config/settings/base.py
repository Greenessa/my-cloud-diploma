import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Функция-помощник для обязательных переменных
def get_env_variable(var_name, default=None, required=False):
    value = os.getenv(var_name, default)
    # Если переменная обязательна и её нет (или она пустая) — падаем
    if required and not value:
        raise ValueError(
            f"КРИТИЧЕСКАЯ ОШИБКА: Переменная окружения {var_name} не задана. "
            f"Проверьте файл .env или настройки сервера."
        )
    return value


SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY", required=True)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    "corsheaders",
    "users",
    "storage.apps.StorageConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators



AUTH_PASSWORD_VALIDATORS = [
    # 1. Проверяет, что пароль не слишком похож на логин/email
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    # 2. Проверяет минимальную длину (по умолчанию 8 символов).
    # Примечание: наш ТЗ требует 6 символов, поэтому минимальную длину 
    # мы зададим через OPTIONS в следующем валидаторе или расслабим здесь.
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 6,  # Устанавливаем 6 символов, как требует ТЗ
        }
    },
    # 3. Проверяет, что пароль не входит в список самых популярных
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    # 4. Проверяет, что пароль не состоит только из цифр
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    # 5. КАСТОМНЫЙ ВАЛИДАТОР (проверяет заглавные, цифры и спецсимволы)
    {
        "NAME": "users.validators.PasswordStrengthValidator",
    },
]



LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
# Наше собственное хранилище файлов облака
# (все файлы будут сохраняться сюда)
CLOUD_STORAGE_DIR = BASE_DIR / os.getenv("CLOUD_STORAGE_DIR", "storage")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

AUTH_USER_MODEL = "users.User"

# --- НАСТРОЙКА ЛОГИРОВАНИЯ ---
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            # Формат: дата и время [уровень] сообщение
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        # Вывод в консоль
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        # Вывод в файл (полезно для продакшена)
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "django.log",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
    },
    "loggers": {
        # Логгер для самого Django
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        # Логгер для нашего приложения (можно использовать в views)
        "users": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "storage": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}