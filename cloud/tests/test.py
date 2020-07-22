from django.views import View
from django.http import JsonResponse
from asset.models import *
from utils import safe_json_dumps
from ..sdk.request import CloudSDKRequest
from ..sdk import CloudSDKClient
from ..configs import cloud_config
import time

class Test(View):

    def get(self, request):
        req = CloudSDKRequest(
            'alicloud', 'query_hosts', {
                'Region': 'cn-shenzhen',
                'Account': 'ksyun_kdxss@ijunhai.com'})

        r = []
        start = time.time()
        # req = CloudSDKRequest('qcloud',
        #                       'query_monitor_data',
        #                       {
        #                           'Region': 'ap-guangzhou',
        #                           'Namespace': 'QCE/CVM',
        #                            'MetricName': 'CPUUsage',
        #                            'Instances': [{
        #                                'Dimensions':[{
        #                                    'Name': 'InstanceId',
        #                                    'Value': 'ins-3axmy46k'
        #                                },{
        #                                    'Name': 'InstanceId',
        #                                    'Value': 'ins-khzqypgq'
        #                                }
        #                                ]
        #                            }],
        #                            'Period': 60,
        #                            'StartTime': '2020-03-21 00:00:00',
        #                            'EndTime': '2020-03-24 00:00:00'
        #                       })
        # #
        # client = CloudSDKClient()
        # resp = client.execute(req)
        # r.extend(resp['data'])
        middle = time.time()
        print(middle-start)

        # req = CloudSDKRequest('alicloud',
        #                       'query_monitor_data',
        #                       {
        #                           'Region': 'cn-shenzhen',
        #                           'Namespace': "acs_ecs_dashboard",
        #                           'MetricName': 'cpu_total',
        #                           'Dimensions': [
        #                               {'instanceId': 'i-wz91xbt2dbgtsxasvpuu'}
        #                           ],
        #                           'Period': 60,
        #                           'StartTime': '2020-03-25 00:00:00',
        #                           'EndTime': '2020-03-28 00:00:00'
        #                       })
        #
        #
        client = CloudSDKClient()
        resp = client.execute(req)
        r.extend(resp['data'])
        end = time.time()
        print(end - middle)
        print(len(r))
        resp = {
            'data': r
        }


        # client = CloudSDKClient()
        # resp = client.execute(req)
        # print(resp)

        return JsonResponse(resp)


