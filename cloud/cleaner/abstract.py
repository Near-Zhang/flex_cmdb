from typing import Optional, Any
from abc import ABC, abstractmethod
from utils import safe_json_loads
from ..sdk import CloudSDKLowLayerRequest


__all__ = ['AbstractCloudCleaner']


class AbstractCloudCleaner(ABC):
    """
    抽象的云清洗器，用于定义统一方法
    """

    def __init__(self, request: CloudSDKLowLayerRequest) -> None:
        """
        初始化
        :param request: 请求对象
        """
        self._req = request
        self._action = request.parent.action
        self._interface = request.parent.interface_conf
        self._origin_resp = None

    def clean(self, resp: dict) -> dict:
        """
        清洗响应数据的入口
        :param resp: 响应数据
        :return:
        """
        # 保存原始响应
        self._origin_resp = resp

        # 若为错误响应则直接返回错误内容作为响应
        if 'Error' in resp:
            return resp['Error']

        # 调用开始钩子
        resp = self._trigger_hook('start', resp)

        # 根据动作类型区分清洗方法，得到清洗后的数据
        action_type = self._action.split('_')[0]
        if action_type == 'query':
            resp = self._clean_query_resp(resp)
        else:
            resp = self._clean_operation_resp(resp)

        # 返回调用结束钩子后的数据
        return self._trigger_hook('end', resp)

    def _trigger_hook(self, hook: str, resp_or_data: dict) -> dict:
        """
        触发钩子对响应进行处理
        :param hook: 钩子配置
        :param resp_or_data: 响应或数据
        :return: 触发钩子处理后的响应
        """
        conf = self._interface['output']['hooks'][hook]
        if conf['method']:
            method = conf['method']
            kwargs = conf['kwargs'] or {}

            if conf['base'] == 'common':
                hook_method = getattr(self, f'_do_{hook}_{method}', None)
            else:
                hook_method = getattr(
                    self, f'_do_{self._action}_{hook}_{method}', None)

            if hook_method:
                resp_or_data = hook_method(resp_or_data, **kwargs)

        return resp_or_data

    def _clean_query_resp(self, resp: dict) -> dict:
        """
        清洗查询类型动作的响应数据
        :param resp: 响应数据
        :return: 清洗后的数据
        """
        # 提取数据列表，若结果为字符串则进行反序列化
        data = self._extract_deep_value(
            self._interface['output']['data'], resp, 0)
        if isinstance(data, str):
            data = safe_json_loads(data)

        # 根据配置进行所以记录的清洗，k 和 v 分别表示最后得到的键和值
        fields = self._interface['output']['fields']
        new_data = []
        num = 0
        for d in data:
            new_d = self._clean_single_query_data(d, num, fields)
            new_data.append(new_d)
            num += 1

        # 获取现有长度和总长度
        current = len(new_data)
        total = resp.get('TotalCount', current)

        # 返回标准结构
        return {
            'total': total,
            'current': current,
            'data': new_data,
        }

    @abstractmethod
    def _clean_operation_resp(self, resp: dict) -> dict:
        """
        清洗操作类型动作的响应数据
        :param resp: 响应数据
        :return: 清洗后数据
        """
        pass

    @staticmethod
    def _extract_deep_value(key: str, data: Any, num: int) -> Any:
        """
        从数据中提取表示多层次键的对应值
        :param key: 多层次键，用 . 表示层次
        :param data: 数据
        :return: 值
        """
        v = data
        for p in key.split('.'):
            if isinstance(v, list):
                try:
                    v = v[num] if p == 'N' else v[int(p)]
                except IndexError:
                    v = None
            else:
                v = v.get(p, None)
            if v is None:
                break
        return v

    def _clean_single_query_data(self, data: dict, num: int, fields: dict) -> dict:
        """
        清洗单条查询结果的数据
        :param data: 单条数据
        :param num: 单条数据编号
        :param fields: 字段配置
        :return: 清洗后的数据
        """
        # 单个键和配置的获取
        new_data = {}
        for k, conf in fields.items():
            src = conf['src']
            key = conf['key']
            mapping = conf['mapping']
            default = conf['default']

            v = None
            # 各个来源来获取值 v，若 key 未设置则返回来源本身
            if src == 'req':
                if key:
                    v = self._extract_deep_value(key, self._req.request_params, num)
                else:
                    v = self._req.request_params

            elif src == 'data':
                if key:
                    v = self._extract_deep_value(key, data, num)
                else:
                    v = data

            elif src == 'method' and key:
                v_method = getattr(self, f'_{key}', None)
                if v_method:
                    v = v_method(data, num)

            # 方法来源的 key 为设置，以及来源未设置，则根据默认方法来获取值 v
            else:
                v_method = getattr(self, f'_get_{self._action}_{k}', None)
                if v_method:
                    v = v_method(data, num)

            # 若值 v 为空 则取默认值
            if v is None:
                v = default
            # 若映射 mapping 已设置，则取映射值，映射失败则使用默认值
            elif mapping:
                v = mapping.get(v, default)

            # 更新键值
            new_data.update({k: v})

        return new_data

    @staticmethod
    def _do_end_make_unique(resp: dict, unique_keys: Optional[list] = None):
        """
        保留联合唯一的记录，利用集合来实现
        :param resp: 响应数据
        :param unique_keys: 联合唯一的键
        :return: 联合唯一的响应数据
        """
        if not isinstance(resp['data'], list):
            return resp

        unique_data = []
        unique_set = set()

        for r in resp['data']:
            kv_list = []
            for k, v in r.items():
                if k in unique_keys:
                    kv_list.append((k, v))

            kv_tuple = tuple(kv_list)
            if kv_tuple not in unique_set:
                unique_set.add(kv_tuple)
                unique_data.append(r)

        current = len(unique_data)
        total = resp['total'] - (current - resp[current])

        return {
            'total': total,
            'current': current,
            'data': unique_data,
        }
