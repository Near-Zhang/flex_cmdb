from django.test import SimpleTestCase
from cloud.native_sdk.qcloud import QcloudNativeSDK
from cloud.models import CloudInterface
from datetime import date


class TestQCloudNativeSDK(SimpleTestCase):
    """
    单元测试
    """

    def setUp(self):
        self.sdk = QcloudNativeSDK()

        # 新 sdk 接口例子
        self.new_interface = {
            'interface': CloudInterface(**{
                'name': 'DescribeZones',
                'module': 'cvm',
                'version': date(2017, 3, 12)}),
            'public_params': {
                'Region': 'ap-shanghai'
            }
        }

        # 老 sdk 接口例子
        self.old_interface = {
            'interface': CloudInterface(**{
                'name': 'DescribeProject',
                'module': 'account',
                'version': None}),
            'public_params': {
                'Region': 'ap-shanghai'
            }
        }

        # 账单接口
        self.bill_interface = {
            'interface': CloudInterface(**{
                'name': 'DescribeBillDetail',
                'module': 'billing',
                'version': date(2018, 7, 9)}),
            'public_params': {
                'Region': 'ap-shanghai'
            },
            'request_params': {
                'PeriodType': 'byPayTime',
                'Offset': 0,
                'Limit': 1,
                'Month': '2020-01'
            }
        }

    def test_not_set(self):
        """
        未设置进行请求，应该报错
        """
        try:
            self.sdk.request()
        except AssertionError:
            pass

    def test_new_interface(self):
        """
        测试新 sdk 负责的接口
        """
        self.sdk.set(**self.new_interface)
        resp = self.sdk.request()
        self.assertIn('TotalCount', resp, 'failed')
        self.assertNotIn('Error', resp, 'failed')

    def test_old_interface(self):
        """
        测试老 sdk 负责的接口
        """
        self.sdk.set(**self.old_interface)
        resp = self.sdk.request()
        self.assertEqual(resp['code'], 0, 'failed')

    def test_bill_interface(self):
        """
        测试账单的接口
        """
        self.sdk.set(**self.bill_interface)
        resp = self.sdk.request()
        # self.assertEqual(resp['code'], 0, 'failed')
        print(resp)

from tencentcloud.billing.v20180709.models import DescribeBillDetailRequest