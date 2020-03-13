from typing import Optional, Tuple, Any
from .abstract import AbstractNativeSDK
import hashlib, requests
from collections import OrderedDict
from utils import safe_json_loads
from config import UCLOUD_KEY


__all__ = ['UCloudNativeSDK']


class UCloudNativeSDK(AbstractNativeSDK):
    """
    优刻得原生 SDK
    https://docs.ucloud.cn/api/summary/overview
    """

    def __init__(self) -> None:
        """
        特有初始化
        """
        super().__init__()

        # 调用地址
        self._url = 'http://api.ucloud.cn/'

    def request(self) -> dict:
        """
        使用原生 sdk 发送请求，返回响应结果
        :return: 包含响应结果的字典
        """
        assert self._already, 'request info has not been set，should use self.set()'

        url = self._url + self._build_url_params() + '&Signature=' + self._get_signature()
        try:
            resp = requests.get(url, timeout=(3, 30))
            data = safe_json_loads(resp.content)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            data = {
                'RetCode': '502',
                'Message': 'sdk request timeout'
            }
        return data

    @property
    def _ak_sk(self) -> Tuple[str, str]:
        """
        获取请求所使用的密钥对
        :return: 返回 access_key、secret_key 密钥对
        """
        return UCLOUD_KEY

    def _build_url_params(self) -> str:
        """
        构造请求参数
        :return: 请求参数字符串
        """
        self._params.update({
            'Action': self._interface['name'],
            'PublicKey': self._ak_sk[0]
        })
        params_list = [k.replace('_', '.') + '=' + self._encode_value(self._params[k]) for k in self._params.keys()]
        return '?' + '&'.join(params_list)

    def _get_signature(self) -> str:
        """
        获取签名
        :return: 签名字符串
        """
        # 排序
        params = OrderedDict(sorted(self._params.items(), key=lambda item: item[0]))

        # 拼接为字符串
        simplified = ""
        for key, value in params.items():
            simplified += str(key) + self._encode_value(value)
        simplified += self._ak_sk[1]

        # 计算哈希值
        hash_new = hashlib.sha1()
        hash_new.update(simplified.encode("utf-8"))
        hash_value = hash_new.hexdigest()
        return hash_value

    @staticmethod
    def _encode_value(v: Any) -> Any:
        """
        完成某些值的字符串转换，以完成签名
        :param v: 参数值
        :return: 转化值
        """
        # bool 转换为小写字符串
        if isinstance(v, bool):
            return "true" if v else "false"

        # 浮点数转化为字符串
        if isinstance(v, float):
            return str(int(v)) if v % 1 == 0 else str(v)
        return str(v)
