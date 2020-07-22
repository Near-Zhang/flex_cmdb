from django.db import models
from common.models import BaseModel


__all__ = ['Count']


class Count(BaseModel):
    """
    资源记录统计信息，通过供应商接口来获取
    """

    class Meta:
        db_table = 'count'
        verbose_name = '统计数'
        unique_together = ('region', 'project', 'interface')
        ordering = ('idc', 'name', 'enable')

    record_num = models.IntegerField(default=0, verbose_name='记录数量')

    # 逻辑外键
    region = models.CharField(default='', max_length=32, verbose_name='地域')
    project = models.CharField(default='', max_length=32, verbose_name='云项目')
    interface = models.CharField(max_length=32, verbose_name='云接口')