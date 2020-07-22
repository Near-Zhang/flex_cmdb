from django.db import models
from common.models import ResourceModel


__all__ = ['IDC']


class IDC(ResourceModel):
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
    comment = models.TextField(null=True, blank=True, verbose_name='备注')
