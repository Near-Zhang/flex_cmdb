from .abstract import AbstractCloudCleaner
from utils import get_datetime_with_tz, safe_json_loads


class ALiCloudCleaner(AbstractCloudCleaner):
    """
    阿里云清洗器
    """

    def _clean_operation_resp(self, resp: dict) -> dict:
        """
        清洗操作类型动作的响应数据
        :param resp: 响应数据
        :return: 清洗后数据
        """
        pass

    ### 查询地域的自定义钩子和字段清洗
    @staticmethod
    def _get_query_zones_state(data: dict, num: int) -> int:
        """
        可用区状态清洗
        :param data: 数据
        :param num: 数据编号
        :return: 状态编号
        """
        available =  data['AvailableResourceCreation']['ResourceTypes']
        if 'Instance' in available:
            return 0
        else:
            return 2

    ### 查询监控数据的自定义钩子和字段清洗
    @staticmethod
    def _do_query_monitor_data_start_hook(resp: dict) -> dict:
        """
        开始钩子，转换其中的时间戳为日期，将值转为百分比
        :param resp: 响应数据
        :return: 清洗后数据
        """
        data = safe_json_loads(resp['Datapoints'])
        for d in data:
            dt = get_datetime_with_tz(d['timestamp'] // 1000)
            d.update({
                'Day': dt.date(),
                'Hour': dt.hour,
                'Minute': dt.minute,
                'Average': d['Average']
            })
        resp['Datapoints'] = data
        return resp

    @staticmethod
    def _get_query_hosts_project(data: dict, num: int) -> str:
        """
        主机项目缩写清洗
        :param data: 数据
        :param num: 数据编号
        :return: 项目缩写
        """
        hostname = data['InstanceName']
        name_list = hostname.split('-')
        if len(name_list) > 3:
            project_flag  = '-'.join(name_list[:2])
        else:
            project_flag = name_list[0]

        return project_flag.lower()

    @staticmethod
    def _get_query_hosts_memory(data: dict, num: int) -> str:
        """
        主机内存转化单位
        :param data: 数据
        :param num: 数据编号
        :return: 项目缩写
        """
        return data['Memory'] / 1024

    @staticmethod
    def _get_query_hosts_public_ip(data: dict, num: int) -> str:
        """
        公有 ip 清洗
        :param data: 数据
        :param num: 数据编号
        :return: ip 信息
        """
        eip = data['EipAddress'].get('IpAddress')
        if not eip:
            pips = data['PublicIpAddress']['IpAddress'] or []
            return ','.join(pips)
        return eip