from __future__ import annotations
from typing import Optional


__all__ = ['CloudSDKResponse']


class CloudSDKResponse:
    """
    云接口 SDK 响应
    """

    def __init__(self, data: Optional[list] = None, total: int = 0) -> None:
        """
        初始化
        :param data: 响应数据
        """
        if data and isinstance(data, list):
            self._data = data
        else:
            self._data = []
        self._total = total
        self._current = len(self._data)

    @property
    def data(self) -> list:
        """
        获取响应数据
        """
        return self._data

    def extend(self, resp: CloudSDKResponse) -> None:
        """
        合并响应，用于多个 SDK 请求的响应
        :param resp: SDK 响应对象
        """
        self._data.extend(resp.data)
        self._current += resp.current
        self._total += resp.total

    def add(self, resp: CloudSDKResponse) -> None:
        """
        叠加响应，用于多个底层请求的响应
        :param resp: SDK 响应对象
        """
        if not self._total:
            self._total = resp.total
        self._data.extend(resp.data)
        self._current += resp.current

    @property
    def total(self) -> int:
        """
        获取当前数据总长度
        """
        return self._total

    @property
    def current(self) -> int:
        """
        获取当前数据长度
        """
        return self._current

    def to_dict(self) -> dict:
        """
        字典转化
        """
        return {
            'total': self._total,
            'current': self._current,
            'data': self.data
        }
