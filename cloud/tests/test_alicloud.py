from django.test import SimpleTestCase
from cloud.native_sdk.alicloud import AlicloudNativeSDK
from cloud.models import CloudInterface
from datetime import date


class TestALiCloudNativeSDK(SimpleTestCase):
    """
    单元测试
    """

    def setUp(self):
        self.sdk = AlicloudNativeSDK()

        # 地域查询，不带区域
        self.region_interface = {
            'interface': CloudInterface(**{
                'name': 'DescribeRegions',
                'module': 'ecs',
                'version': date(2014, 5, 26)}),
            'public_params': {}
        }

        # 可用区查询，带区域
        self.zone_interface = {
            'interface': CloudInterface(**{
                'name': 'DescribeZones',
                'module': 'ecs',
                'version': date(2014, 5, 26)}),
            'public_params': {
                'Region': 'default'
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

    def test_region_interface(self):
        """
        测试地域查询的接口
        """
        self.sdk.set(**self.region_interface)
        resp = self.sdk.request()
        self.assertIn('Regions', resp)

    def test_zone_interface(self):
        """
        测试可用区查询的接口
        """
        self.sdk.set(**self.zone_interface)
        resp = self.sdk.request()
        self.assertIn('Zones', resp)
