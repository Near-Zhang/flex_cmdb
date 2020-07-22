from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
import event.routing


websocket_urlpatterns = [
    path(r'event/', event.routing.websocket_urlpatterns)
]


application = ProtocolTypeRouter({
    # (默认 http 转发到 django views)
    'websocket': URLRouter(websocket_urlpatterns)
})
