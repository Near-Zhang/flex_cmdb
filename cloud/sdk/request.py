from __future__ import annotations
from typing import List, Optional, Any
from ..configs.core import cloud_config
from ..exceptions import CloudSDKRequestError
from copy import deepcopy
from math import ceil


__all__ = ['CloudSDKRequest', 'CloudSDKInterRequest']


class CloudSDKRequest:
    """
    云接口 SDK 请求
    """

    def __init__(self,
                 idc: str,
                 action: str,
                 params: Optional[dict] = None,
                 region_type: str = 'single',
                 total: int = 0) -> None:
        """
        请求信息初始化
        :param idc: 供应商对象
        :param action: 云动作标识
        :param params: 请求参数
        :param region_type: 地域查询类型，single 单个地域；massive 为有效地域；all 所有地域
        :param total: 指定所访问存在分页的接口的记录总数，以进行并发访问
        """
        # 对外属性设置，包括配置提取
        self.idc = idc
        self.action = action

        self.idc_conf = cloud_config[idc]['settings']
        self.action_conf = cloud_config[idc]['actions'][action]['settings']
        self.interface_conf = cloud_config[idc]['actions'][action]['interface']

        # 对内属性设置
        self._params = deepcopy(params) if params else {}
        self._region_type = region_type
        self._action_type = action.split('_')[0]
        self._total = total

        # 包含内部请求的列表
        self._inter_requests = []

        # 开始构建内部请求
        self._build_inter_requests()

    def get_inter_requests(self) -> List[CloudSDKInterRequest]:
        """
        获取内部请求列表
        :return: 包含内部请求的列表
        """
        return self._inter_requests

    def _add_inter_request(self, req_params: dict) -> None:
        """
        添加内部请求
        """
        inter_req = CloudSDKInterRequest(self, req_params)
        self._inter_requests.append(inter_req)

    def _build_inter_requests(self) -> None:
        """
        构造子请求参数的列表
        """
        # 区分是否为多地域请求
        if self._region_type == 'single':
            self._build_single_region_request()

        # 只有查询动作才支持多地域请求
        elif self._action_type == 'query':
            self._build_multi_region_request()

        else:
            raise CloudSDKRequestError(
                'only single request supports Non query action')

    def _build_single_region_request(self) -> None:
        """
        构建单地域请求
        """
        req_params = {}
        req_params.update(self._params)

        paging = self.action_conf['paging']
        if self._total and paging:
            self._paging_request()
        else:
            # 加入内部请求列表
            self._add_inter_request(req_params)

    def _build_multi_region_request(self) -> None:
        """
        构建多地域请求
        """
        pass

    def _paging_request(self) -> None:
        """
        将请求构造成多个访问不同分页的子请求
        """
        limit_str = self.idc_conf['limit_str']
        limit = self.idc_conf['limit_max']
        offset_str = self.idc_conf['offset_str']
        offset = self.idc_conf['offset_init']
        paging_base = self.idc_conf['paging_base']

        # 向上取整得到总共的页数
        page_number = int(ceil(float(self._total) / limit))

        # 根据需要请求的页数生成内部请求
        for page in range(page_number):
            p = deepcopy(self._params)
            p.update({
                limit_str: limit,
                offset_str: offset
            })
            self._add_inter_request(p)
            if paging_base == 'page':
                offset += 1
            else:
                offset += limit

    def __len__(self) -> int:
        """
        返回内部请求列表长度
        :return: 长度
        """
        return len(self._inter_requests)

    def __getitem__(self, item) -> CloudSDKInterRequest:
        """
        返回内部请求列表对应索引
        :return: 长度
        """
        return self._inter_requests[item]


class CloudSDKInterRequest:
    """
    云接口 SDK 内部请求
    """

    def __init__(self,
                 parent: CloudSDKRequest,
                 req_params: Optional[dict] = None) -> None:
        """
        初始化
        :param parent: 父请求对象
        :param req_params: 请求参数
        """
        self.request_params = deepcopy(req_params) if req_params else {}
        self.parent = parent

    def get(self, item: str, default: Any = None):
        """
        获取参数值
        :param item: 参数键
        :param default: 默认值
        :return: 参数值
        """
        return self.request_params.get(item, default)
