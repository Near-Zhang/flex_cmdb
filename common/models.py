from django.db import models


class BaseModel(models.Model):
    """
    基础抽象模型
    """

    class Meta:
        verbose_name = '基础抽象模型'
        abstract = True


class ResourceModel(BaseModel):
    """
    资源抽象模型
    """

    class Meta:
        verbose_name = '资源抽象模型'
        abstract = True

    # 公共字段
    uuid = models.CharField(max_length=32, primary_key=True, verbose_name='UUID')
    created_by = models.CharField(max_length=32, verbose_name='创建用户UUID')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_by = models.CharField(max_length=32, null=True, verbose_name='更新用户UUID')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class SoftDeleteModel(ResourceModel):
    """
    软删除资源抽象模型
    """

    class Meta:
        verbose_name = '软删除抽象模型'
        abstract = True

    # 软删除公共字段
    deleted_by = models.CharField(max_length=32, null=True, verbose_name='删除用户UUID')
    deleted_at = models.DateTimeField(auto_now=True, verbose_name='删除时间')
