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
            'alicloud', 'query_hosts', region_mode=0, record_count=0, **{
                'Region': 'cn-shanghai'
            })

        # for r in req:
        #     print(r.params)


        client = CloudSDKClient()
        resp = client.execute(req)

        print(resp.data)
        print(resp.total)
        print(resp.current)

        return JsonResponse(resp.to_dict())


