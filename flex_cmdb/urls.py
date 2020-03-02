from django.urls import re_path, include
from asset.views import *


urlpatterns = [
    re_path('asset/', include('asset.urls', namespace="asset")),
]
