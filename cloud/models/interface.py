from django.db import models
from common.models import BaseModel


__all__ = ['CloudInterface']


class CloudInterface(BaseModel):
    """
    云接口，对于不通云进行不同操作的执行接口，提供这些信息到实际云提供的 SDK 中以完成请求，需手动录入
    (asset.IDC, CloudAction) -o2o-> CloudInterface
    """

    class Meta:
        db_table = 'cloud_interface'
        verbose_name = '云接口'
        unique_together = ('idc', 'cloud_action')
        ordering = ('idc', 'cloud_action', 'enable')

    name = models.CharField(max_length=255, verbose_name='名字')
    module = models.CharField(max_length=255, null=True, verbose_name='模块')
    version = models.DateField(null=True, verbose_name='版本日期')
    freq_limit = models.IntegerField(null=True, verbose_name='请求频率限制')
    sp_paging = models.BooleanField(default=False, verbose_name='是否支持分页')
    enable = models.BooleanField(default=True, verbose_name='是否启用')
    comment = models.TextField(null=True, blank=True, verbose_name='备注')

    # 逻辑外键
    idc = models.CharField(max_length=32, verbose_name='供应商')
    cloud_action = models.CharField(max_length=32, verbose_name='云动作')