from typing import Tuple
from .abstract import AbstractNativeSDK
from ..exceptions import CloudNativeSDKError
from utils import dynamic_import_class, safe_json_loads
from config import ALICLOUD_KEY

# AliCloud sdk
from aliyunsdkcore.client import AcsRequest, AcsClient
from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException


__all__ = ['ALiCloudNativeSDK']


class ALiCloudNativeSDK(AbstractNativeSDK):
    """
    阿里云原生 SDK
    https://developer.aliyun.com/tools/sdk?spm=a2c4g.11186623.2.11.10996b3cvemP9z#/python
    """

    def __init__(self) -> None:
        """
        特有初始化
        """
        super().__init__()

        # 默认地域
        self._default_region = 'cn-hangzhou'


    def request(self) -> dict:
        """
        使用原生 sdk 发送请求，返回响应结果
        :return: 包含响应结果的字典
        """
        assert self._already, 'request info has not been set，should use self.set()'

        request = self._get_req()
        client = self._get_client()
        try:
            response = client.do_action_with_exception(request)
        except ServerException as e:
            return self._build_error_data(e)
        except ClientException as e:
            raise CloudNativeSDKError(f'client error: {e.error_code}, {e.message}')

        return safe_json_loads(response)

    @property
    def _ak_sk(self) -> Tuple[str, str]:
        """
        获取请求所使用的密钥对
        :return: 返回 access_key、secret_key 密钥对
        """
        return ALICLOUD_KEY

    def _get_client(self) -> AcsClient:
        """
        生成客户端，并返回客户端对象
        :return: 客户端对象
        """
        # 即使地域不起作用时，该 sdk 也必须传入地域参数，先查看请求参数中是否包含地域，否则取默认值
        region = self._params.get('Region', self._default_region)
        return AcsClient(self._ak_sk[0], self._ak_sk[1], region)

    def _get_req(self) -> AcsRequest:
        """
        生成请求对象
        :return: 请求对象
        """
        # 提取接口信息
        name = self._interface['name']
        md = self._interface['module']
        version = self._interface['version']

        # 动态获取请求类
        req_class_path = f'aliyunsdk{md}.request.{version}.{name}Request'
        req_class_name = f'{name}Request'
        req_class = dynamic_import_class(f'{req_class_path}.{req_class_name}')

        # 实例化请求对象，并导入请求参数
        assert req_class, f'request class {req_class_path}.{req_class_name} has not been import'
        request = req_class()
        request.set_query_params(self._params)
        request.set_accept_format("json")
        return request

    @staticmethod
    def _build_error_data(e: ServerException) -> dict:
        """
        根据异常来构造响应
        :param e: 异常对象
        :return: 响应字典
        """
        return {
            'Error': {
                'Code': e.error_code,
                'Message': e.message,
                'RequestId': e.request_id
            }
        }
