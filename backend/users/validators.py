import re

from django.core.exceptions import ValidationError


USERNAME_REGEX = re.compile(r"^[a-zA-Z][a-zA-Z0-9]{3,19}$")


def validate_username(value):
    if not USERNAME_REGEX.match(value):
        raise ValidationError(
            "Логин должен содержать только латинские буквы и цифры, "
            "начинаться с буквы и быть длиной от 4 до 20 символов."
        )


def validate_password_strength(value):
    if len(value) < 6:
        raise ValidationError("Пароль должен содержать не менее 6 символов.")
    if not re.search(r"[A-Z]", value):
        raise ValidationError("Пароль должен содержать хотя бы одну заглавную букву.")
    if not re.search(r"\d", value):
        raise ValidationError("Пароль должен содержать хотя бы одну цифру.")
    if not re.search(r"[^A-Za-z0-9]", value):
        raise ValidationError("Пароль должен содержать хотя бы один специальный символ.")


class PasswordStrengthValidator:
    """
    Валидатор пароля для AUTH_PASSWORD_VALIDATORS.
    Django сам вызывает его при создании/смене пароля.
    """

    def validate(self, password, user=None):
        validate_password_strength(password)

    def get_help_text(self):
        return (
            "Пароль должен содержать не менее 6 символов, "
            "хотя бы одну заглавную букву, одну цифру "
            "и один специальный символ."
        )