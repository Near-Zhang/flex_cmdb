from django.db import models
from common.models import DisplayModel


__all__ = ['Region', 'Zone']


# 地域状态
RegionState = (
    '可用'
    '测试中'
    '不可用'
)


class Region(DisplayModel):
    """
    地域信息，通过云接口同步
    IDC - o2m -> Region
    """

    class Meta:
        db_table = 'region'
        verbose_name = '地域'
        unique_together = (('idc', 'name'), ('idc', 'flag'))
        ordering = ('idc', 'name', 'enable')

    flag = models.CharField(max_length=255, verbose_name='标识')
    name = models.CharField(max_length=255, verbose_name='名字')
    state = models.IntegerField(verbose_name='状态')
    enable = models.BooleanField(default=True, verbose_name='是否启用')
    comment = models.TextField(null=True, verbose_name='备注')

    # 逻辑外键
    idc = models.CharField(max_length=32, verbose_name='供应商UUID')


class Zone(DisplayModel):
    """
    可用区信息，通过云接口同步
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