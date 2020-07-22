from django.urls import re_path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    re_path('asset/', include('asset.urls')),
    re_path('cloud/', include('cloud.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
