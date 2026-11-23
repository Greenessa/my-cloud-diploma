"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("storage.urls")),
]

if settings.DEBUG:
    # Медиафайлы
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Явная раздача JS и CSS из папки assets (чтобы не было 404)
    urlpatterns += [
        re_path(r'^assets/(?P<path>.*)$', serve, {
            'document_root': settings.BASE_DIR.parent / "frontend" / "dist" / "assets",
        }),
        # Явная раздача favicon и других файлов из корня dist
        re_path(r'^(?P<path>favicon\.svg|icons\.svg)$', serve, {
            'document_root': settings.BASE_DIR.parent / "frontend" / "dist",
        }),
    ]

# Ловушка для SPA. 
# Исключаем api, admin, media, static, assets и файлы svg
urlpatterns += [
    re_path(r'^(?!api/|admin/|media/|static/|assets/|favicon\.svg|icons\.svg).*$', TemplateView.as_view(template_name="index.html")),
]