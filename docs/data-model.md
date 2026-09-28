# Модели данных

## User

| Поле | Тип | Ограничения |
|---|---|---|
| id | AutoField | Primary Key идентификатор строки таблицы
|username|Charfield(20)| уникальный, [a-zA-Z][a-zA-Z0-9]{3,19} |
|full_name|CharField(255) | обязательное |
|email|EmailField | уникальный, валидный |
|password|CharField(128)|хэш пароля На входе валидируется: ≥6 симв., 1 заглавная, 1 цифра, 1 спецсимвол |
|is_admin|BooleanField| по умолчанию False |
|storage_path| CharField(255) | относительный путь к папке пользователя |

## File
| Поле | Тип | Описание |
|---|---|---|
| id | AutoField | Primary Key идентификатор строки таблицы
| owner | ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) | владелец файла |
|file_name|CharField(255)| как загрузил пользователь |
|stored_name| CharField(64) | сгенерированное UUID-имя файла на диске |
| size | BigIntegerField | размер в байтах |
| uploaded_at | DateTimeField | дата загрузки файла |
| last_downloaded_at | DateTimeField | дата последнего скачивания, может быть пустым null=True |
| comment |TextField(blank=True)| комментарий к файлу (blank=True может быть пустой) |
| file_path * | CharField(512) | относительный путь к файлу |
| share_token | UUIDField(unique=True) | уникальный, для публичной ссылки |

* Примечание: file_path строится как f"{user.storage_path}/{stored_name}",
например: "user_5/a1b2c3d4-....bin"