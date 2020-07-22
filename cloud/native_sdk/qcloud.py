from typing import Tuple, List
from .abstract import AbstractNativeSDK
from ..exceptions import CloudNativeSDKError
from utils import dynamic_import_class, safe_json_dumps, safe_json_loads
from config import QCLOUD_KEY

# QCloud 新 sdk
from tencentcloud.common.credential import Credential
from tencentcloud.common.abstract_client import AbstractClient
from tencentcloud.common.abstract_model import AbstractModel
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

# QCloud 老 sdk
from QcloudApi.qcloudapi import QcloudApi


__all__ = ['QCloudNativeSDK']


class QCloudNativeSDK(AbstractNativeSDK):
    """
    腾讯云原生 SDK
    https://cloud.tencent.com/document/sdk/Python#api-explorer
    """

    def __init__(self) -> None:
        """
        特有初始化
        """
        super().__init__()

        # 用于缓存对象
        self._credential = None
        self._http_config = None
        self._client_config = None

    def request(self) -> dict:
        """
        使用原生 sdk 发送请求，返回响应结果，根据接口区分使用新老两版 sdk
        :return: 包含响应结果的字典
        """
        assert self._already, 'request info has not been set，should use self.set()'

        if self._interface['name'] in self._old_interface:
            return self._old_request()
        else:
            return self._request()

    @property
    def _old_interface(self) -> List[str]:
        return ['DescribeProject', 'AddProject']

    def _request(self) -> dict:
        """
        使用新版 sdk 发送请求，返回响应结果
        :return: 包含响应结果的字典
        """
        # 分别获取客户端对象、请求对象
        client = self._get_client()
        req = self._get_req()

        # 进行请求，得到响应
        try:
            resp = getattr(client, self._interface['name'])(req)
        except TencentCloudSDKException as e:
            if not e.requestId:
                raise CloudNativeSDKError(f'client error: {e.message}')
            return self._build_error_data(e)

        # 将结果反序列化为对象并输出
        return safe_json_loads(resp.to_json_string())

    def _old_request(self) -> dict:
        """
        使用老版 sdk 发送请求，返回响应结果
        :return: 包含响应结果的字典
        """
        # 传入密钥，获取客户端
        secret_params = ({
            'secretId': self._ak_sk[0],
            'secretKey': self._ak_sk[1]
        })
        client = QcloudApi(self._interface['module'], secret_params)
        client.generateUrl(self._interface['name'], self._params)

        # 进行请求，得到响应
        try:
            resp = client.call(self._interface['name'], self._params)
        except TencentCloudSDKException as e:
            if not e.requestId:
                raise CloudNativeSDKError(f'client error: {e.message}')
            return self._build_error_data(e)

        # 将结果反序列化为对象并输出
        return safe_json_loads(resp)

    def _get_credential(self) -> Credential:
        """
        通过 ak 和 sk，实例化认证对象
        :return: 认证对象
        """
        secret = {
            'secretId': self._ak_sk[0],
            'secretKey': self._ak_sk[1]
        }
        return Credential(**secret)

    @property
    def _ak_sk(self) -> Tuple[str, str]:
        """
        获取请求所使用的密钥对
        :return: 返回 access_key、secret_key 密钥对
        """
        return QCLOUD_KEY

    def _get_client(self) -> AbstractClient:
        """
        初始化客户端，并返回客户端对象
        :return: 客户端对象
        """
        # 获取认证对象
        if not self._credential:
            self._credential = self._get_credential()

        # 获取客户端配置，包括 http 配置
        if not self._client_config:
            if not self._http_config:
                self._http_config = self._get_http_config()
            self._client_config = ClientProfile(httpProfile=self._http_config)

        # 获取接口信息
        md = self._interface['module']
        version = self._interface['version']

        # 动态获取客户端类
        client_module_path = f'tencentcloud.{md}.{version}.{md}_client'
        client_class_name = f'{md.capitalize()}Client'
        client_class = dynamic_import_class(
            f'{client_module_path}.{client_class_name}')

        # 实例化客户端对象
        region = self._params.get('Region')
        return client_class(self._credential, region, self._client_config)

    def _get_req(self) -> AbstractModel:
        """
        生成请求对象
        :return: 请求对象
        """
        # 获取接口信息
        name = self._interface['name']
        md = self._interface['module']
        version = self._interface['version']

        # 动态获取请求类
        req_class_path = f'tencentcloud.{md}.{version}.models'
        req_class_name = f'{name}Request'
        req_class = dynamic_import_class(f'{req_class_path}.{req_class_name}')

        # 实例化请求对象，并导入请求参数
        assert req_class, 'request class has not been import, check cloud_interface object'
        req = req_class()
        param_json = safe_json_dumps(self._params)
        req.from_json_string(param_json)
        return req

    @staticmethod
    def _get_http_config(**kwargs) -> HttpProfile:
        """
        初始化 http 配置
        :return: HttpProfile
        """
        config = HttpProfile(**kwargs)
        return config

    def _build_error_data(self, e: TencentCloudSDKException) -> dict:
        """
        根据异常来构造响应
        :param e: 异常对象
        :return: 响应字典
        """
        code = e.code or 'Unknown',
        msg = e.message or 'Unknown'
        return self._standard_error_data(code, msg)
