from __future__ import annotations
from typing import Optional, Any
from yaml import load, FullLoader
import os


__all__ = ['CloudConfig', 'cloud_config']


class SingletonMeta(type):
    """
    单例元类
    """

    _instance: Optional[CloudConfig] = None

    def __call__(cls, *args, **kwargs) -> CloudConfig:
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class CloudConfig(metaclass=SingletonMeta):
    """
    云配置单例类
    """

    def __init__(self) -> None:
        """
        初始化配置存储字典
        """
        self._config = {}
        d = os.path.dirname(__file__)
        for f in os.listdir(d):
            if f.endswith('.yaml'):
                idc = f.split('.')[0]
                path = f'{d}/{f}'
                config = load(open(path), Loader=FullLoader)
                self._config.update({idc: config})


    def get(self, key: str, default: Optional[str] = None) -> Any:
        """
        通过方法查询配置
        :param key: 查询键
        :param default: 默认值
        :return: 结果值
        """
        return self._config.get(key, default)

    def __getitem__(self, item: str) -> Any:
        """
        通过索引查询配置
        :param item: 查询键
        :return: 结果值
        """
        return self._config.get(item)


# 外部使用的实例，直接加载实例的话可以不需要单例
cloud_config = CloudConfig()