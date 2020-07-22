__all__ = ['CloudSDKResponse']


class CloudSDKResponse:
    """
    云接口 SDK 响应
    """

    def __init__(self, resp):
        """
        初始化
        :param resp: 响应结果
        """
        self._resp = resp

    @property
    def data(self):
        """
        获取数据列表
        """
        return self._resp['data']

    @property
    def current(self):
        """
        获取当前数据长度
        """
        return self._resp['current']

    @property
    def total(self):
        """
        获取当前数据总长度
        """
        return self._resp['total']

    def origin(self):
        """
        获取原始响应
        :return: 响应结果
        """
        return self._resp
