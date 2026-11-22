from rest_framework import serializers

from .models import File


class FileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения данных файла.
    Отдаёт все нужные поля, кроме служебных путей.
    """
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    share_url = serializers.SerializerMethodField()  

    class Meta:
        model = File
        fields = [
            "id",
            "owner",
            "owner_username",
            "file_name",
            "size",
            "comment",
            "uploaded_at",
            "last_downloaded_at",
            "share_token",
            "share_url",  
        ]
        read_only_fields = [
            "id",
            "owner",
            "owner_username",
            "size",
            "uploaded_at",
            "last_downloaded_at",
            "share_token",
            "share_url", 
        ]

    def get_share_url(self, obj):
        """Формирует полный URL для публичного скачивания."""
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/api/share/{obj.share_token}/")
        return f"/api/share/{obj.share_token}/"

class FileUploadSerializer(serializers.Serializer):
    """
    Сериализатор загрузки файла.
    Принимает файл и комментарий.
    """
    file = serializers.FileField(required=True)
    comment = serializers.CharField(required=False, allow_blank=True)


class FileUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор изменения имени и комментария.
    """
    class Meta:
        model = File
        fields = ["file_name", "comment"]