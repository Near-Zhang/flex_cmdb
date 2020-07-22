from django.db import models
from common.models import BaseModel


__all__ = ['Image']


class Image(BaseModel):
    """
    镜像信息，通过供应商接口来获取和同步
    """

    class Meta:
        db_table = 'image'
        verbose_name = '镜像'
        unique_together = ('region', 'flag')
        ordering = ('region', 'name')

    # 镜像信息
    flag = models.CharField(max_length=255, verbose_name='标识')
    name = models.CharField(max_length=255, verbose_name='名字')
    type = models.CharField(max_length=255, verbose_name='类型')
    source = models.CharField(max_length=255, verbose_name='来源')
    size = models.IntegerField(verbose_name='大小，单位GB')
    state = models.CharField(max_length=255, verbose_name='状态')
    description = models.CharField(max_length=255, verbose_name='描述')
    creator = models.CharField(null=True, max_length=255, verbose_name='创建者')
    created_time = models.DateTimeField(null=True, verbose_name='创建时间')

    # 系统信息
    os_name = models.CharField(max_length=255, verbose_name='系统名')
    architecture = models.CharField(max_length=255, verbose_name='架构')
    platform = models.CharField(max_length=255, verbose_name='平台')
    is_support_cloud_init = models.CharField(max_length=255, verbose_name='是否支持云初始化')

    # 逻辑外键
    region = models.CharField(max_length=32, verbose_name='地域')