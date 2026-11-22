from django.shortcuts import render
from .permissions import IsAdmin, IsAdminOrSelf
from .serializers import AdminUserSerializer, AdminUserUpdateSerializer
from rest_framework.generics import get_object_or_404
from .models import User

from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)


class RegisterView(APIView):
    """
    POST /api/auth/register/
    Регистрация нового пользователя.
    Доступна без авторизации.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Сразу логиним нового пользователя
        login(request, user)
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    POST /api/auth/login/
    Вход в систему. Создаёт сессию.
    Доступна без авторизации.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Выход из системы. Удаляет сессию.
    Только для авторизованных.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    """
    GET /api/auth/me/
    Возвращает данные текущего пользователя.
    Только для авторизованных.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
    

class UserListView(APIView):
    """
    GET /api/users/
    Список всех пользователей (только для админа).
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = User.objects.all().order_by("id")
        serializer = AdminUserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    """
    GET /api/users/{id}/ — данные пользователя (админ или сам).
    PATCH /api/users/{id}/ — изменить is_admin (только админ).
    DELETE /api/users/{id}/ — удалить пользователя (только админ).
    """
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk):
        user = self.get_object(pk)
        self.check_object_permissions(request, user)
        serializer = AdminUserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk):
        # Только админ может менять других пользователей
        if not request.user.is_admin:
            return Response(
                {"error": "Только администратор может изменять пользователей."},
                status=status.HTTP_403_FORBIDDEN,
            )
        user = self.get_object(pk)
        serializer = AdminUserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(AdminUserSerializer(user).data)

    def delete(self, request, pk):
        if not request.user.is_admin:
            return Response(
                {"error": "Только администратор может удалять пользователей."},
                status=status.HTTP_403_FORBIDDEN,
            )
        user = self.get_object(pk)
        # Запретим админу удалять самого себя
        if user == request.user:
            return Response(
                {"error": "Нельзя удалить самого себя."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)