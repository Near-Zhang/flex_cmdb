from common.serializers import ResourceSerializer, BulkListSerializer
from rest_framework_bulk import BulkSerializerMixin
from ..models import IDC, Region, Zone


__all__ = ['IDCSerializer', 'RegionSerializer', 'ZoneSerializer']


class IDCSerializer(BulkSerializerMixin, ResourceSerializer):
    """
    供应商模型序列化器
    """

    class Meta:
        list_serializer_class = BulkListSerializer
        update_lookup_field = 'uuid'
        fields = '__all__'
        model = IDC


class RegionSerializer(BulkSerializerMixin, ResourceSerializer):
    """
    地域模型序列化器
    """

    class Meta:
        list_serializer_class = BulkListSerializer
        update_lookup_field = 'uuid'
        fields = '__all__'
        model = Region


class ZoneSerializer(BulkSerializerMixin, ResourceSerializer):
    """
    可用区模型序列化器
    """

    class Meta:
        list_serializer_class = BulkListSerializer
        update_lookup_field = 'uuid'
        fields = '__all__'
        model = Zone