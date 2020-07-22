from django.db import models
from common.models import BaseModel


__all__ = ['Project']


class Project(BaseModel):
    """
    项目信息，通过供应商接口来获取
    IDC - o2m -> Project
    """
    class Meta:
        db_table = 'project'
        verbose_name = '项目'
        unique_together = (('idc', 'name'), ('idc', 'flag'))
        ordering = ('idc', 'name', 'enable')

    name = models.CharField(max_length=255, verbose_name='名字')
    flag = models.CharField(max_length=255, verbose_name='标识')
    massive = models.BooleanField(default=True, verbose_name='是否有内容')
    enable = models.BooleanField(default=True, verbose_name='是否启用')
    comment = models.TextField(null=True, verbose_name='备注')

    # 逻辑外键
    idc = models.CharField(max_length=32, verbose_name='供应商')

    # project = models.CharField(null=True, max_length=64, verbose_name='项目')
    # delete = models.IntegerField(null=False, default=False)
    # is_main = models.BooleanField(default=False, verbose_name='主简写')
    # updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # created_time = models.DateTimeField(null=True, verbose_name='创建时间')
    # md5 = models.CharField(max_length=255, db_index=True, unique=True, verbose_name='校验id')
    # uuid = models.CharField(max_length=255, db_index=True, unique=True, verbose_name='唯一id')
    # generated_time = models.DateTimeField(auto_now_add=True, verbose_name='生成时间')