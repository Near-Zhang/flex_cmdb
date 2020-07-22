from .abstract import AbstractCloudCleaner
from utils import get_datetime_with_tz


class QCloudCleaner(AbstractCloudCleaner):
    """
    腾讯云清洗器
    """

    def _clean_operation_resp(self, resp: dict) -> dict:
        """
        清洗操作类型动作的响应数据
        :param resp: 响应数据
        :return: 清洗后数据
        """
        pass

    ### 查询数据信息的自定义钩子和字段清洗
    @staticmethod
    def _get_query_hosts_public_ip(data: dict, num: int) -> str:
        """
        公有 ip 清洗
        :param data: 数据
        :param num: 数据编号
        :return: ip 信息
        """
        pips = data['PublicIpAddresses'] or []
        return ','.join(pips)

    ### 查询监控数据的自定义钩子和字段清洗
    @staticmethod
    def _do_query_monitor_data_start_hook(resp: dict) -> dict:
        """
        开始钩子，转换其中的时间戳为日期，并和 values 列表进行合并
        :param resp: 响应数据
        :return: 清洗后数据
        """
        new_values = []
        timestamps = resp['DataPoints'][0]['Timestamps']
        values = resp['DataPoints'][0]['Values']

        i = 0
        for ts in timestamps:
            dt = get_datetime_with_tz(ts)
            v = values[i]
            new_value = {
                'Day': dt.date(),
                'Hour': dt.hour,
                'Minute': dt.minute,
                'Value': v
            }
            new_values.append(new_value)
            i += 1

        resp['DataPoints'][0]['Values'] = new_values
        return resp

    def _get_query_monitor_data_host(self, data: dict, num: int) -> str:
        """
        可用区状态字段清洗
        :param data: 数据
        :param num: 数据编号
        :return: 状态编号
        """
        return self._origin_resp['DataPoints'][0]['Dimensions'][0]['Value']

