from rest_framework_bulk.routes import BulkRouter
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .tests.test import Test


# django 定义路由
urlpatterns = format_suffix_patterns([
    # 路由条目
    path('test/region/', Test.as_view())
])

# 框架注册路由
router = BulkRouter()

# 合并路由
urlpatterns.extend(router.urls)