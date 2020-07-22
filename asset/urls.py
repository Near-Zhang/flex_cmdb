from rest_framework_bulk.routes import BulkRouter
from rest_framework.urlpatterns import format_suffix_patterns
from .viewsets import *


# django 定义路由
urlpatterns = format_suffix_patterns([
    # 路由条目
])

# 框架注册路由
router = BulkRouter()
router.register('idc', IDCViewSet)
router.register('regions', RegionViewSet)
router.register('zones', ZoneViewSet)

# 合并路由
urlpatterns.extend(router.urls)

