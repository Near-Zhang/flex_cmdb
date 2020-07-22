from django.test import TestCase
from utils import DAO
from asset.models import IDC
from ..models import CloudAction
from ..sdk.reuqest import CloudSDKRequest


class TestSDKClient(TestCase):
    """
    单元测试
    """

    def setUp(self):
        # 获取供应商和动作
        self.idc = DAO(IDC).get_obj(flag='qcloud')
        self.action = DAO(CloudAction).get_obj(flag='query_region')

    def test_get_request(self):
        """
        未设置进行请求，应该报错
        """
        req = CloudSDKRequest(self.idc, self.action)
        print(req)