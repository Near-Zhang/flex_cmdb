from __future__ import annotations
from typing import List, Optional, Any, Iterable, Union
from ..configs import cloud_config
from ..exceptions import CloudSDKRequestError
from asset.models import Region
from math import ceil


__all__ = [
    'CloudSDKRequest',
    'CloudSDKLowLayerRequest'
]


class CloudSDKRequest:
    """
    云 SDK 请求
    """

    def __init__(self,
                 csp: str,
                 action: str,
                 region_mode: int = 0,
                 record_count: int = 0,
                 **kwargs) -> None:
        """
        请求信息初始化
        :param csp: 云供应商标识
        :param action: 动作标识
        :param region_mode: 地域查询模式，0 单个地域；1 有效地域；2 所有地域
、      :param record_count: 请求的记录数量，方便直接进行分页并发访问
        :param kwargs: 请求参数
        """
        # 属性设置
        self.csp = csp
        self.action = action

        # 配置提取
        self.csp_conf = cloud_config[csp]['settings']
        self.action_conf = cloud_config[csp]['actions'][action]['settings']
        self.interface_conf = cloud_config[csp]['actions'][action]['interface']

        # 私有属性设置
        self._action_type, self._record_name = action.split('_')
        self._region_mode = region_mode
        self._record_count = record_count
        self._params = kwargs

        # 所有子请求，可以全部是请求对象，也可以全部是真正进行处理的底层请求
        self._child_requests = None

    def get_child_requests(self) -> List[CloudSDKChildRequest]:
        """
        获取子请求列表
        :return: 子请求列表
        """
        if self._child_requests is None:
            self._build_child_requests()
        return self._child_requests

    def redo_paging_request(self, record_count):
        """
        重新分页
        :param record_count: 记录数
        :return: 子请求列表
        """
        self._record_count = record_count
        paging_required = self.action_conf['paging_required']
        if self._record_count and paging_required:
            self._child_requests = self._paging_request()

    def _build_child_requests(self) -> None:
        """
        构建子请求
        """
        # 互斥参数验证
        err = self._validate()
        if err:
            raise CloudSDKRequestError(err)

        # 根据区域模式进行子请求构建
        region_required = self.action_conf['region_required']
        if self._region_mode == 0 or not region_required:
            self._build_single_region_child_requests()
        else:
            self._build_multi_region_child_requests()

    def _validate(self) -> Optional[list]:
        """
        互斥参数验证
        :return: 错误信息或错误信息列表
        """
        error = []

        # 只有查询类型的动作支持多区域模式
        if self._action_type != 'query' and self._region_mode != 0:
            error.append(
                'only query action_type supports setting multi region_mode')

        # 只有单区域模式支持设置记录数量
        if self._region_mode != 0 and self._record_count != 0:
            error.append(
                'only single region_mode supports setting record_count')

        return error

    def _build_single_region_child_requests(self) -> None:
        """
        构建单区域子请求
        """
        # 当动作需要分页并已设置了记录数目，则进行分页
        paging_required = self.action_conf['paging_required']
        if self._record_count and paging_required:
            self._child_requests = self._paging_request()

        # 直接加入子请求列表
        else:
            self._child_requests = [
                CloudSDKLowLayerRequest(
                    self, **self._params)]

    def _build_multi_region_child_requests(self) -> None:
        """
        构建多区域子请求
        """
        # 提取配置
        region_str = self.csp_conf['region_str']

        # 只针对有资源的区域进行遍历，冗余一页减少再次查询
        if self._region_mode == 2:
            regions_with_records = []
            child_request = [
                CloudSDKRequest(self.csp,
                                self.action,
                                rc + self.csp_conf['limit_max'],
                                **self._params,
                                **{region_str: region})
                for region, rc in regions_with_records
            ]

        # 对所有资源的区域进行遍历
        else:
            regions = Region.dao.get_field_value('flag')
            child_request = [
                CloudSDKRequest(self.csp,
                                self.action,
                                0,
                                **self._params,
                                **{region_str: region})
                for region in regions
            ]

        self._child_requests = child_request

    def _paging_request(self) -> List[CloudSDKLowLayerRequest]:
        """
        将请求构造成多个访问不同分页的子请求
        """
        # 配置提取
        limit_str = self.csp_conf['limit_str']
        limit = self.csp_conf['limit_max']
        offset_str = self.csp_conf['offset_str']
        offset = self.csp_conf['offset_init']
        paging_base = self.csp_conf['paging_base']

        # 构造子请求列表
        child_requests = []

        # 向上取整得到总共的页数
        page_number = int(ceil(float(self._record_count) / limit))

        # 根据页数生成子请求
        for page in range(page_number):
            paging_params = {
                limit_str: limit,
                offset_str: offset
            }
            child_requests.append(
                CloudSDKLowLayerRequest(
                    self,
                    **self._params,
                    **paging_params))

            if paging_base == 'page':
                offset += 1
            else:
                offset += limit

        return child_requests

    def __iter__(self) -> Iterable[CloudSDKChildRequest]:
        """
        返回包含子请求的迭代器
        :return: 迭代器
        """
        if self._child_requests is None:
            self._build_child_requests()
        return iter(self._child_requests)

    def __len__(self) -> int:
        """
        返回内部请求列表长度
        :return: 长度
        """
        if self._child_requests is None:
            self._build_child_requests()
        return len(self._child_requests)

    def __getitem__(self, item) -> CloudSDKChildRequest:
        """
        返回内部请求列表对应索引
        :return: 子请求
        """
        if self._child_requests is None:
            self._build_child_requests()
        return self._child_requests[item]


class CloudSDKLowLayerRequest:
    """
    云 SDK 底层请求，存在于请求的子请求中，是真正被处理的
    """

    def __init__(self,
                 parent: CloudSDKRequest,
                 **kwargs) -> None:
        """
        初始化
        :param parent: 父请求对象
        :param req_params: 子请求参数
        """
        self.parent = parent
        self.params = kwargs

    def get(self, item: str, default: Any = None) -> Any:
        """
        获取参数值
        :param item: 参数键
        :param default: 默认值
        :return: 参数值
        """
        return self.params.get(item, default)


# 子请求类型
CloudSDKChildRequest = Union[CloudSDKLowLayerRequest, CloudSDKRequest]
