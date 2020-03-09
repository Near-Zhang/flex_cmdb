from django.db import models
from common.models import ResourceModel


__all__ = ['CloudAction']


class CloudAction(ResourceModel):
    """
    云动作信息，归纳可对云进行的操作动作，需自行录入
    """

    class Meta:
        db_table = 'cloud_action'
        verbose_name = '云动作'
        ordering = ('name', 'enable')

    name = models.CharField(max_length=255, unique=True, verbose_name='名字')
    flag = models.CharField(max_length=255, unique=True, verbose_name='标识')
    type = models.IntegerField(default=0, verbose_name='类型，0 为查询类型，1 为操作类型')
    region_required = models.BooleanField(default=False, verbose_name='是否需要地域参数')
    project_required = models.BooleanField(default=False, verbose_name='是否需要项目参数')
    storage_required = models.BooleanField(default=False, verbose_name='是否需要存储')
    enable = models.BooleanField(default=True, verbose_name='是否启用')
    comment = models.TextField(null=True, blank=True, verbose_name='备注')
