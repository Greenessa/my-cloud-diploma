# Модели данных

## User

| Поле | Тип | Ограничения |
|---|---|---|
| id | AutoField | Primary Key идентификатор строки таблицы
|username|Charfield(20)| уникальный, [a-zA-Z][a-zA-Z0-9]{3,19} |
|full_name|CharField(255) | обязательное |
|email|EmailField | уникальный, валидный |
|pasword|CharField(128)|хэш пароля На входе валидируется: ≥6 симв., 1 заглавная, 1 цифра, 1 спецсимвол |
|is_admin|BooleanField| по умолчанию False |
|storage_path| CharField(255) | относительный путь к папке пользователя |

## File
| Поле | Тип | Описание |
|---|---|---|
| id | AutoField | Primary Key идентификатор строки таблицы
| owner | ForeignKey(User, on_delete=models.CASCADE) | владелец файла |
|file_name|CharField(255)| как загрузил пользователь |
|storage_name| CharField(64) | оригинальное имя на диске (UUID) |
| size | BigIntegerField | размер в байтах |
|create_date| DateTimeField | дата загрузки файла |
|lastload_date| DateTimeField | дата последнего скачивания, может быть пустым null=True, blank=True |
|comment|TextField(300)| blank=True может быть пустой |
| file_path | CharField(512) | относительный путь к файлу |
| share_token | UUIDField(unique=True) | уникальный, для публичной ссылки |
