from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.urls import re_path

from chat import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("chat.urls")),
    path("accounts/", include("account.urls")),
    re_path(r'^api/v1/', include('api.urls', namespace="api")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
