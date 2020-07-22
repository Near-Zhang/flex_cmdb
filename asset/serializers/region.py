from common.serializers import ResourceSerializer, BulkListSerializer
from rest_framework_bulk import BulkSerializerMixin
from ..models import Region, Zone


__all__ = ['RegionSerializer', 'ZoneSerializer']


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