# My Cloud — облачное хранилище

Дипломный проект по профессии «Fullstack-разработчик на Python».

Веб-приложение для хранения, загрузки, скачивания, переименования
и удаления файлов, с возможностью делиться файлами по публичной ссылке
и административным интерфейсом для управления пользователями.

## Стек

- **Бэкенд:** Python 3.10+, Django, PostgreSQL, DRF (Django REST Framework)
- **Фронтенд:** JavaScript/TypeScript, React, Redux, React Router, Vite
- **Развёртывание:** reg.ru

## Функциональность

- Регистрация и аутентификация пользователей (сессии).
- Административный интерфейс: список пользователей, удаление, смена
  признака «администратор», просмотр хранилищ пользователей.
- Файловое хранилище: загрузка, скачивание, переименование,
  удаление, изменение комментария, публичная ссылка на файл.
- SPA-интерфейс на React.

## Структура репозитория

```
my-cloud/
├── backend/               # Django-проект
│   ├── config/            # настройки проекта (settings, urls, wsgi, asgi)
│   ├── users/             # приложение пользователей
│   ├── storage/           # приложение файлового хранилища
│   ├── manage.py
│   └── requirements.txt
├── frontend/              # React + Vite
│   ├── public/
│   ├── src/
│   │   ├── api/           # слой работы с API
│   │   ├── assets/
│   │   ├── components/
│   │   ├── pages/
│   │   └── store/         # Redux
│   ├── package.json
│   └── vite.config.ts
├── docs/                  # проектная документация
│   ├── data-model.md      # модели данных
│   ├── api.md             # спецификация API
│   ├── stage-2.md         # инструкция по установке Python и Django
│   ├── stage-2-postgresql-install.md
│   ├── stage-2-postgresql.md
│   ├── stage-2-settings.md
│   ├── stage-3-models.md
│   └── stage-4-auth-api.md
├── .gitignore
└── README.md
```

## Особенности интеграции фронтенда и бэкенда

Для работы сессионной аутентификации с Django REST Framework при кросс-доменных запросах необходимо выполнить два условия:

**1. Включить отправку credentials (cookie)**
На бэкенде настроено `CORS_ALLOW_CREDENTIALS = True`. На фронтенде при использовании `axios` нужно установить глобальную настройку:
```javascript
axios.defaults.withCredentials = true;
```
Или для `fetch`:
```javascript
fetch(url, { credentials: 'include' })
```

**2. Передавать CSRF-токен для небезопасных методов**
Django REST Framework использует `SessionAuthentication`, которая требует CSRF-токен для запросов `POST`, `PUT`, `PATCH`, `DELETE`.

Токен хранится в cookie с именем `csrftoken`. Фронтенд должен извлечь его и передать в заголовке `X-CSRFToken`.

Пример функции для получения токена из cookie:
```javascript
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
```

Пример настройки axios (через interceptor или в конкретном запросе):
```javascript
const csrftoken = getCookie('csrftoken');
axios.post('/api/files/', data, {
    headers: {
        'X-CSRFToken': csrftoken,
    }
});
```
*(Для `multipart/form-data` (загрузка файлов) можно передавать токен в поле формы `csrfmiddlewaretoken`, но заголовок `X-CSRFToken` работает универсально).*

## Установка и запуск

> 🚧 Раздел заполнится по мере готовности бэкенда и фронтенда.

## Развёртывание на reg.ru

> 🚧 Раздел заполнится на финальном этапе.

## API

> 🚧 Список эндпоинтов будет добавлен после реализации.

## Автор

Романова Маргарита Алексеевна
группа FPY-124
2026 год
