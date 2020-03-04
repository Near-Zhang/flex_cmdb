from rest_framework.serializers import ModelSerializer
from rest_framework_bulk import BulkSerializerMixin
from ..models import IDC, Region, Zone


__all__ = ['IDCSerializer', 'RegionSerializer', 'ZoneSerializer']


class IDCSerializer(BulkSerializerMixin, ModelSerializer):
    """
    供应商模型序列化器
    """

    class Meta(object):
        fields = '__all__'
        model = IDC


class RegionSerializer(BulkSerializerMixin, ModelSerializer):
    """
    地域模型序列化器
    """

    class Meta(object):
        fields = '__all__'
        model = Region


class ZoneSerializer(BulkSerializerMixin, ModelSerializer):
    """
    可用区模型序列化器
    """

    class Meta(object):
        fields = '__all__'
        model = Zone