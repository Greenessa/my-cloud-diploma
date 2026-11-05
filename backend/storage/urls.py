from django.urls import path

from .views import (
    FileDetailView,
    FileDownloadView,
    FileListCreateView,
    FileShareView,
    PublicDownloadView,
)

app_name = "storage"

urlpatterns = [
    path("files/", FileListCreateView.as_view(), name="file-list"),
    path("files/<int:pk>/", FileDetailView.as_view(), name="file-detail"),
    path("files/<int:pk>/download/", FileDownloadView.as_view(), name="file-download"),
    path("files/<int:pk>/share/", FileShareView.as_view(), name="file-share"),
    path("share/<uuid:token>/", PublicDownloadView.as_view(), name="public-download"),
]