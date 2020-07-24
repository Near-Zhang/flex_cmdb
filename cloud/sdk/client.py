from .request import CloudSDKRequest, CloudSDKLowLayerRequest
from .response import CloudSDKResponse
from concurrent.futures import ThreadPoolExecutor
from threading import BoundedSemaphore
from ..exceptions import CloudSDKClientError
from utils import datetime_to_timestamp, dynamic_import_class
import time
import os


__all__ = ['CloudSDKClient']


# 限制动作的信号量
semaphore_map = {}


class CloudSDKClient:
    """
    云 SDK 客户端
    """

    def __init__(self) -> None:
        """
        初始化执行器
        """
        core = os.cpu_count()
        self._executor = ThreadPoolExecutor(core)

    def execute(self, request: CloudSDKRequest) -> CloudSDKResponse:
        """
        执行请求
        :param request: 请求对象
        :return: 响应对象
        """
        # 响应对象
        full_response = CloudSDKResponse()

        # 根据子请求类型进行处理
        # 子请求是底层请求则并行处理，叠加数据后合并得到完整响应
        if isinstance(request[0], CloudSDKLowLayerRequest):
            # 根据第一个响应确定分页，并执行构建分页请求
            result = self._low_layer_execute(request[0])
            total = result.get('total')
            request.redo_paging_request(total)
            full_response.extend(self._concurrent_execute(request))

        # 子请求是 SDK 请求则递归处理，合并所有响应得到完整响应
        else:
            for child_req in request:
                full_response.extend(self.execute(child_req))

        return full_response

    def _concurrent_execute(
            self,
            request: CloudSDKRequest) -> CloudSDKResponse:
        """
        为所有底层进行多线程执行和汇总
        :param request: 请求对象
        :return: 响应结果
        """
        # 根据第一个响应确定分页
        resp = CloudSDKResponse()
        full_error = []
        results = self._executor.map(self._low_layer_execute, iter(request))
        for result in results:
            try:
                data = result.get('data')
                # 叠加数据，更新总数
                if data:
                    resp.add(CloudSDKResponse(data, result['total']))
                else:
                    full_error.append(result)
            except Exception as e:
                full_error.append(e.args)

        if full_error:
            raise CloudSDKClientError(full_error)

        return resp

    @staticmethod
    def _low_layer_execute(request: CloudSDKLowLayerRequest):
        """
        执行单个底层请求
        :param request: 内部请求对象
        :return: 响应结果
        """
        # 获取原生 sdk 对象
        csp = request.parent.csp
        action = request.parent.action
        sdk_name = request.parent.csp_conf['native_sdk']
        native_sdk_path = f'cloud.native_sdk.{csp}.{sdk_name}'
        native_sdk = dynamic_import_class(native_sdk_path)()

        # 设置并请求
        native_sdk.set(request.parent.interface_conf, request.params)
        req_limit = request.parent.csp_conf['req_limit']
        key = f'{csp}:{action}'
        if not semaphore_map.get(key):
            semaphore_map[key] = BoundedSemaphore(req_limit)
        sp = semaphore_map.get(key)

        # 用于计算消耗时间
        start_time = datetime_to_timestamp()
        try_time = 3
        resp = None

        # 请求重试机制
        while try_time:
            with sp:
                resp = native_sdk.request()

            # 得到消耗时间
            end_time = datetime_to_timestamp()
            expend_time = end_time - start_time

            # 将请求消耗时间控制在1秒左右，防止请求频率过高
            if expend_time < 1:
                time.sleep(1 - expend_time)

            if 'Error' in resp:
                try_time -= 1
            else:
                break

        # 预处理原始数据
        cleaner_name = request.parent.csp_conf['cleaner']
        cleaner_path = f'cloud.cleaner.{csp}.{cleaner_name}'
        cleaner = dynamic_import_class(cleaner_path)(request)
        data = cleaner.clean(resp)

        # 返回数据
        return data
