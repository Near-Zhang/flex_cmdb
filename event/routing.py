from channels.routing import URLRouter
from django.urls import re_path
from .consumers import *


websocket_urlpatterns = URLRouter([
    re_path(r'^ws/jobs/((?P<uuid>\w+)/)?$', JobConsumer)
])