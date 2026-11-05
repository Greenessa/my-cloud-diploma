import os
import logging
from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsAdmin
from .models import File
from .permissions import IsOwnerOrAdmin
from .serializers import (
    FileSerializer,
    FileUpdateSerializer,
    FileUploadSerializer,
)
from .services import save_file_to_disk

logger = logging.getLogger(__name__)


class FileListCreateView(APIView):
    """
    GET: список файлов (своих, а для админа — с ?owner={id})
    POST: загрузка файла (multipart/form-data)
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        owner_id = request.query_params.get("owner")
        
        if owner_id:
            if not request.user.is_admin:
                return Response(
                    {"error": "Только администратор может смотреть чужие файлы."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            files = File.objects.filter(owner_id=owner_id)
            logger.info(f"Админ {request.user.username} смотрит файлы пользователя {owner_id}")
        else:
            files = File.objects.filter(owner=request.user)
            logger.debug(f"Пользователь {request.user.username} запросил список своих файлов")
            
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        uploaded_file = serializer.validated_data["file"]
        comment = serializer.validated_data.get("comment", "")
        
        stored_name, file_path, size = save_file_to_disk(uploaded_file, request.user)
        
        file_obj = File.objects.create(
            owner=request.user,
            file_name=uploaded_file.name,
            stored_name=stored_name,
            size=size,
            comment=comment,
            file_path=file_path,
        )
        
        logger.info(f"Пользователь {request.user.username} загрузил файл {file_obj.file_name}")
        return Response(FileSerializer(file_obj).data, status=status.HTTP_201_CREATED)


class FileDetailView(APIView):
    """
    GET: метаданные файла
    PATCH: переименовать / изменить комментарий
    DELETE: удалить файл
    """
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self, pk):
        return get_object_or_404(File, pk=pk)

    def get(self, request, pk):
        file_obj = self.get_object(pk)
        self.check_object_permissions(request, file_obj)
        return Response(FileSerializer(file_obj).data)

    def patch(self, request, pk):
        file_obj = self.get_object(pk)
        self.check_object_permissions(request, file_obj)
        
        serializer = FileUpdateSerializer(file_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        logger.info(f"Пользователь {request.user.username} изменил файл {file_obj.id}")
        return Response(FileSerializer(file_obj).data)

    def delete(self, request, pk):
        file_obj = self.get_object(pk)
        self.check_object_permissions(request, file_obj)
        
        file_name = file_obj.file_name
        file_obj.delete()  # сигнал post_delete удалит физический файл
        
        logger.info(f"Пользователь {request.user.username} удалил файл {file_name}")
        return Response(status=status.HTTP_204_NO_CONTENT)


class FileDownloadView(APIView):
    """
    GET: скачивание файла с проверкой прав.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request, pk):
        file_obj = get_object_or_404(File, pk=pk)
        self.check_object_permissions(request, file_obj)
        
        full_path = os.path.join(settings.CLOUD_STORAGE_DIR, file_obj.file_path)
        
        if not os.path.exists(full_path):
            logger.error(f"Файл не найден на диске: {full_path}")
            return Response({"error": "Файл не найден на диске"}, status=status.HTTP_404_NOT_FOUND)
            
        # Обновляем дату последнего скачивания
        from django.utils import timezone
        file_obj.last_downloaded_at = timezone.now()
        file_obj.save(update_fields=["last_downloaded_at"])
        
        logger.info(f"Пользователь {request.user.username} скачал файл {file_obj.file_name}")
        
        # Отдаём файл с оригинальным именем
        response = FileResponse(open(full_path, "rb"), as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{file_obj.file_name}"'
        return response


class FileShareView(APIView):
    """
    GET: получить публичную ссылку на файл.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request, pk):
        file_obj = get_object_or_404(File, pk=pk)
        self.check_object_permissions(request, file_obj)
        
        share_url = request.build_absolute_uri(f"/api/share/{file_obj.share_token}/")
        logger.info(f"Пользователь {request.user.username} получил ссылку на файл {file_obj.file_name}")
        return Response({"share_url": share_url})


class PublicDownloadView(APIView):
    """
    GET: скачивание по публичной ссылке (без авторизации).
    """
    permission_classes = [AllowAny]

    def get(self, request, token):
        file_obj = get_object_or_404(File, share_token=token)
        
        full_path = os.path.join(settings.CLOUD_STORAGE_DIR, file_obj.file_path)
        
        if not os.path.exists(full_path):
            return Response({"error": "Файл не найден"}, status=status.HTTP_404_NOT_FOUND)
            
        from django.utils import timezone
        file_obj.last_downloaded_at = timezone.now()
        file_obj.save(update_fields=["last_downloaded_at"])
        
        logger.info(f"Публичное скачивание файла {file_obj.file_name}")
        
        response = FileResponse(open(full_path, "rb"), as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{file_obj.file_name}"'
        return response