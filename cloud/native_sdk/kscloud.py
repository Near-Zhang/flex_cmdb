from typing import Tuple
from .abstract import AbstractNativeSDK
from config import KSCLOUD_KEY

# KSCloud sdk
from kscore.session import get_session


__all__ = ['KSCloudNativeSDK']


class KSCloudNativeSDK(AbstractNativeSDK):
    """
    金山云原生 SDK
    https://docs.ksyun.com/documents/5735
    SDK 模块需要自行下载：https://github.com/KscSDK/ksc-sdk-python
    """

    def __init__(self) -> None:
        """
        特有初始化
        """
        super().__init__()

        # 定义使用默认账号，由于公司在金山云存在多个账号以区分项目，属于定制化
        self._default_account = 'ksyun_kdxss@ijunhai.com'
        # 默认地域
        self._default_region = 'cn-beijing-6'

    def request(self) -> dict:
        """
        使用原生 sdk 发送请求，返回响应结果
        :return: 包含响应结果的字典
        """
        assert self._already, 'request info has not been set，should use self.set()'

        region = self._params.get('Region', self._default_region)
        session = get_session()
        client = session.create_client(self._interface['module'],
                                       region_name=region,
                                       ks_access_key_id=self._ak_sk[0],
                                       ks_secret_access_key=self._ak_sk[1])

        return getattr(client, self._interface['name'])()

    @property
    def _ak_sk(self) -> Tuple[str, str]:
        """
        获取请求所使用的密钥对
        :return: 返回 access_key、secret_key 密钥对
        """
        account = self._params.get('Account', self._default_region)
        return KSCLOUD_KEY.get(account)