# My Cloud — облачное хранилище

Дипломный проект по профессии «Fullstack-разработчик на Python».

Веб-приложение для хранения, загрузки, скачивания, переименования и удаления файлов, с возможностью делиться файлами по публичной ссылке и административным интерфейсом для управления пользователями.

## Стек

- **Бэкенд:** Python 3.11, Django 5.x, PostgreSQL 16, Django REST Framework (DRF).
- **Фронтенд:** React 18, TypeScript, Vite, Redux Toolkit, React Router.
- **Развёртывание:** reg.ru (или любой VPS с Linux).

## Функциональность

- Регистрация и аутентификация пользователей (сессии).
- Административный интерфейс: список пользователей, удаление, смена признака «администратор», просмотр хранилищ пользователей.
- Файловое хранилище: загрузка, скачивание, переименование, удаление, изменение комментария, публичная ссылка на файл.
- SPA-интерфейс на React.

## Структура репозитория

```
my-cloud/
├── backend/               # Django-проект
│   ├── config/            # настройки проекта (settings, urls, wsgi, asgi)
│   ├── users/             # приложение пользователей
│   ├── storage/           # приложение файлового хранилища
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example       # образец переменных окружения
├── frontend/              # React + Vite
│   ├── src/
│   │   ├── api/           # слой работы с API
│   │   ├── components/    # переиспользуемые компоненты
│   │   ├── pages/         # страницы приложения
│   │   └── store/         # Redux
│   ├── package.json
│   └── vite.config.ts
├── docs/                  # проектная документация
│   ├── data-model.md      # модели данных
│   └── api.md             # спецификация API
├── .gitignore
└── README.md
```

## Предварительные требования

Для запуска проекта на компьютере должны быть установлены:

- **Python 3.11+**
- **PostgreSQL 14+** (или новее)
- **Node.js 18+** и **npm**
- **Git**

## Особенности интеграции фронтенда и бэкенда

Для работы сессионной аутентификации с Django REST Framework при кросс-доменных запросах необходимо выполнить два условия:

**1. Включить отправку credentials (cookie)**
На бэкенде настроено `CORS_ALLOW_CREDENTIALS = True`. На фронтенде при использовании `axios` нужно установить глобальную настройку:
```javascript
axios.defaults.withCredentials = true;
```

**2. Передавать CSRF-токен для небезопасных методов**
Django REST Framework использует `SessionAuthentication`, которая требует CSRF-токен для запросов `POST`, `PUT`, `PATCH`, `DELETE`.

Токен хранится в cookie с именем `csrftoken`. Фронтенд должен извлечь его и передать в заголовке `X-CSRFToken`. В нашем React-коде это уже реализовано в `frontend/src/api/client.ts` через `axios.interceptors`.

## Установка и запуск (локально)

### 1. Клонирование репозитория

```bash
git clone https://github.com/ВАШ_ЛОГИН/my-cloud.git
cd my-cloud
```

### 2. Настройка бэкенда

Перейдите в папку бэкенда:

```bash
cd backend
```

Создайте и активируйте виртуальное окружение:

```bash
python -m venv .venv
source .venv/bin/activate  # для macOS/Linux
# .venv\Scripts\activate   # для Windows
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

### 3. Настройка базы данных PostgreSQL

Войдите в консоль PostgreSQL (от имени суперпользователя `postgres`):

```bash
psql postgres
```

Выполните команды (замените `mypassword` на свой пароль):

```sql
CREATE DATABASE my_cloud;
CREATE USER my_cloud_user WITH PASSWORD 'mypassword';
ALTER ROLE my_cloud_user SET client_encoding TO 'utf8';
ALTER ROLE my_cloud_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE my_cloud_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE my_cloud TO my_cloud_user;
\c my_cloud
GRANT ALL ON SCHEMA public TO my_cloud_user;
\q
```

### 4. Настройка переменных окружения (.env)

В папке `backend/` создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Откройте `.env` и заполните своими значениями:

```env
# Django
DJANGO_SECRET_KEY=ваш-сгенерированный-ключ
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=my_cloud
DB_USER=my_cloud_user
DB_PASSWORD=mypassword
DB_HOST=localhost
DB_PORT=5432

# Storage
CLOUD_STORAGE_DIR=storage

# Frontend (CORS и CSRF)
CORS_ALLOWED_ORIGINS=http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173
```

> **Сгенерировать SECRET_KEY:** `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

### 5. Применение миграций и создание администратора

```bash
python manage.py migrate
python manage.py createsuperuser
```

Укажите логин, email и пароль (требования: не менее 6 символов, заглавная буква, цифра, спецсимвол).

### 6. Запуск бэкенда

```bash
python manage.py runserver
```

Бэкенд будет доступен по адресу: `http://127.0.0.1:8000/`

### 7. Настройка и запуск фронтенда

Откройте **новый терминал** (не закрывая бэкенд) и перейдите в папку фронтенда:

```bash
cd frontend
```

Установите зависимости:

```bash
npm install
```

Создайте файл `.env` (на основе `.env.example`):

```bash
cp .env.example .env
```

Убедитесь, что там указан адрес бэкенда:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Запустите dev-сервер:

```bash
npm run dev
```

Фронтенд будет доступен по адресу: `http://localhost:5173/`

### 8. Проверка работоспособности

Откройте `http://localhost:5173/` в браузере. Вы должны увидеть главную страницу My Cloud. Попробуйте войти под созданным администратором.

## Развёртывание на reg.ru

> **Примечание:** раздел описывает общий подход для VPS с Linux. Конкретные шаги могут отличаться в зависимости от тарифа reg.ru. Если вы используете shared-хостинг (не VPS), потребуется уточнить у поддержки reg.ru поддержку Python и PostgreSQL.

### 1. Подготовка сервера

Подключитесь к серверу по SSH:

```bash
ssh user@your-server-ip
```

Установите Python, PostgreSQL, Node.js, Nginx:

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv postgresql nginx git -y
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y
```

### 2. Клонирование проекта

```bash
cd /var/www
git clone https://github.com/ВАШ_ЛОГИН/my-cloud.git
cd my-cloud
```

### 3. Настройка бэкенда

```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Создайте БД (аналогично шагу 3 локальной установки).

Создайте `.env` по образцу `.env.example`, но укажите:

```env
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=ваш-домен.reg.ru
CORS_ALLOWED_ORIGINS=https://ваш-домен.reg.ru
CSRF_TRUSTED_ORIGINS=https://ваш-домен.reg.ru
```

Примените миграции и соберите статику:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 4. Сборка фронтенда

```bash
cd ../frontend
npm install
npm run build
```

После сборки появится папка `dist/`. Скопируйте её содержимое в папку, которую будет раздавать Nginx (например, `/var/www/my-cloud/frontend/dist`).

### 5. Настройка Gunicorn (для бэкенда)

Установите Gunicorn:

```bash
source ../backend/.venv/bin/activate
pip install gunicorn
```

Запустите Gunicorn (в фоне):

```bash
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --daemon
```

### 6. Настройка Nginx

Создайте конфиг `/etc/nginx/sites-available/my-cloud`:

```nginx
server {
    listen 80;
    server_name ваш-домен.reg.ru;

    # Статика Django (админка, DRF)
    location /static/ {
        alias /var/www/my-cloud/backend/staticfiles/;
    }

    # Файлы пользователей (если раздаются через Django, иначе — через Nginx)
    location /media/ {
        alias /var/www/my-cloud/backend/media/;
    }

    # Фронтенд (React SPA)
    location / {
        root /var/www/my-cloud/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API-запросы — проксируем в Gunicorn
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Админка Django
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Активируйте конфиг и перезапустите Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/my-cloud /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. Проверка

Откройте `http://ваш-домен.reg.ru` в браузере. Приложение должно работать.

## API

Полная спецификация API доступна в [docs/api.md](docs/api.md).

Основные эндпоинты:

- `POST /api/auth/register/` — регистрация.
- `POST /api/auth/login/` — вход.
- `POST /api/auth/logout/` — выход.
- `GET /api/auth/me/` — текущий пользователь.
- `GET /api/files/` — список файлов (для админа с `?owner={id}`).
- `POST /api/files/` — загрузка файла (multipart/form-data).
- `GET /api/files/{id}/` — метаданные файла.
- `PATCH /api/files/{id}/` — переименование / изменение комментария.
- `DELETE /api/files/{id}/` — удаление.
- `GET /api/files/{id}/download/` — скачивание.
- `GET /api/files/{id}/share/` — получить публичную ссылку.
- `GET /api/share/{token}/` — скачивание по публичной ссылке (без авторизации).

## Автор

Романова Маргарита Алексеевна
группа FPY-124
2026 год
