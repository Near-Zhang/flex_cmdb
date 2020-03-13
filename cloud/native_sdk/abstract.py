from typing import Optional
from abc import ABC, abstractmethod
from ..exceptions import CloudNativeSDKError


class AbstractNativeSDK(ABC):
    """
    抽象的云原生 sdk，用于定义统一方法
    """

    def __init__(self):
        """
        初始化
        """
        # 请求相关信息
        self._interface = {}
        self._params = {}
        self._already = False


    def set(self, interface: dict, params: Optional[dict] = None) -> None:
        """
        设置请求必要的信息
        :param interface: 包含接口信息的字典
        :param params: 包含请求参数的字典
        """
        # 设置属性
        if interface: self._interface.update(interface)
        if params: self._params.update(params)

        # 检查入参
        input_params = self._interface['input_params']
        if input_params:
            missing_param = set(input_params) - set(self._params)
            if len(missing_param) > 0:
                raise CloudNativeSDKError(f'param {missing_param} is required')

        # 设置可用标识
        self._already = True

    @abstractmethod
    def request(self) -> dict:
        """
        使用原生 sdk 发送请求，返回响应结果
        :return: 包含响应结果的字典
        """
        pass
