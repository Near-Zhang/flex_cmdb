from django.urls import re_path, include


urlpatterns = [
    re_path('asset/', include('asset.urls', namespace="asset")),
]
