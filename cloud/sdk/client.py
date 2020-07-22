from .request import CloudSDKRequest, CloudSDKInterRequest
from .response import CloudSDKResponse
from concurrent.futures import ThreadPoolExecutor
from ..exceptions import CloudSDKClientError
from utils import datetime_to_timestamp, dynamic_import_class
import time


__all__ = ['CloudSDKClient']


class CloudSDKClient:
    """
    云接口 SDK 客户端
    """

    def __init__(self):
        pass

    def execute(self, request: CloudSDKRequest) -> CloudSDKResponse:
        """
        执行请求对象
        :param request: 请求对象
        :return: 响应对象
        """
        # 处理请求
        resp = self._concurrent_execute(request)
        # print(resp)

        # 返回响应
        return CloudSDKResponse(resp)

    def _concurrent_execute(self, request: CloudSDKRequest):
        """
        为所有子请求进行多线程执行和汇总
        :param request: 请求对象
        :return: 响应结果
        """
        # 获取请求访问次数，和请求数量
        inter_req_count = len(request)
        req_limit = request.idc_conf['req_limit']
        if inter_req_count == 1:
            try:
                resp = self._execute_inter_req(request[0])
            except Exception as e:
                raise CloudSDKClientError(*e.args)
            return resp
        elif req_limit > inter_req_count:
            req_limit = inter_req_count
            all_data = []
            all_error = []
            with ThreadPoolExecutor(req_limit) as executor:
                results = executor.map(self._execute_inter_req, request.get_inter_requests())
                total = 0
                for rst in results:
                    try:
                        if rst.get('data'):
                            all_data.extend(rst['data'])
                            total = rst['total']
                        else:
                            all_error.append(rst)
                    except Exception as e:
                        raise CloudSDKClientError(*e.args)

            return {
                'total': total,
                'current': len(all_data),
                'data': all_data
            }

    def _execute_inter_req(self, inter_req: CloudSDKInterRequest):
        """
        执行单个内部请求
        :param inter_req: 内部请求对象
        :return: 响应结果
        """
        # 用于计算消耗时间
        start_time = datetime_to_timestamp()

        # 获取原生 sdk 对象
        idc_flag = inter_req.parent.idc
        sdk_name = inter_req.parent.idc_conf['native_sdk']
        native_sdk_path = f'cloud.native_sdk.{idc_flag}.{sdk_name}'
        native_sdk = dynamic_import_class(native_sdk_path)()

        # 设置并请求
        native_sdk.set(inter_req.parent.interface_conf, inter_req.request_params)
        resp = native_sdk.request()

        # 得到消耗时间
        end_time = datetime_to_timestamp()
        expend_time = end_time - start_time

        # 将请求消耗时间控制在1秒左右，防止请求频率过高
        if expend_time < 1:
            time.sleep(1 - expend_time)

        # 预处理原始数据
        cleaner_name = inter_req.parent.idc_conf['cleaner']
        cleaner_path = f'cloud.cleaner.{idc_flag}.{cleaner_name}'
        cleaner = dynamic_import_class(cleaner_path)(inter_req)
        data = cleaner.clean(resp)

        # 返回数据
        return data
