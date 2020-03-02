from django.db import models
from common.models import BaseModel


__all__ = ['IDC', 'Region', 'Zone']


class IDC(BaseModel):
    """
    供应商信息，通过自行录入
    """

    class Meta:
        db_table = 'idc'
        verbose_name = '供应商'
        ordering = ('name', 'enable')

    flag = models.CharField(max_length=64, unique=True, verbose_name='标识')
    name = models.CharField(max_length=64, unique=True, verbose_name='名字')
    enable = models.BooleanField(default=True, verbose_name='是否启用')
    comment = models.TextField(null=True, verbose_name='备注')


class Region(BaseModel):
    """
    地域信息，通过云接口同步和获取
    IDC - o2m -> Region
    """

    class Meta:
        db_table = 'region'
        verbose_name = '地域'
        unique_together = (('idc', 'name'), ('idc', 'flag'))
        ordering = ('idc', 'name', 'enable')

    flag = models.CharField(max_length=255, verbose_name='标识')
    name = models.CharField(max_length=255, verbose_name='名字')
    state = models.CharField(max_length=255, verbose_name='状态')
    enable = models.BooleanField(default=True, verbose_name='是否启用')
    comment = models.TextField(null=True, verbose_name='备注')

    # 逻辑外键
    idc = models.CharField(max_length=32, verbose_name='供应商UUID')


class Zone(BaseModel):
    """
    可用区信息，通过云接口同步和获取
    Region - o2m -> Zone
    """

    class Meta:
        db_table = 'zone'
        verbose_name = '可用区'
        unique_together = (('region', 'name'), ('region', 'flag'))
        ordering = ('region', 'name', 'enable')

    flag = models.CharField(max_length=255, verbose_name='标识')
    name = models.CharField(max_length=255, verbose_name='名字')
    state = models.CharField(max_length=255, verbose_name='状态')
    enable = models.BooleanField(default=True, verbose_name='是否启用')
    comment = models.TextField(null=True, verbose_name='备注')

    # 逻辑外键
    region = models.CharField(max_length=32, verbose_name='区域UUID')