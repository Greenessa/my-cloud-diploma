from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User
from .validators import validate_password_strength, validate_username


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения данных пользователя (без пароля).
    Используется в ответах API.
    """
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "full_name",
            "email",
            "is_admin",
            "storage_path",
        ]
        read_only_fields = ["id", "is_admin", "storage_path"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации.
    Принимает username, full_name, email, password.
    Сам проверяет все требования из ТЗ.
    """
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ["username", "full_name", "email", "password"]

    def validate_username(self, value):
        validate_username(value)
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Такой логин уже занят.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Такой email уже зарегистрирован.")
        return value

    def validate_password(self, value):
        validate_password_strength(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data["full_name"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Сериализатор входа.
    Принимает username и password, возвращает user при успехе.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs):
        user = authenticate(
            username=attrs["username"],
            password=attrs["password"],
        )
        if not user:
            raise serializers.ValidationError("Неверный логин или пароль.")
        if not user.is_active:
            raise serializers.ValidationError("Пользователь заблокирован.")
        attrs["user"] = user
        return attrs

