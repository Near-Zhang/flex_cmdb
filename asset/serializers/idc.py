from common.serializers import ResourceSerializer, BulkListSerializer
from rest_framework_bulk import BulkSerializerMixin
from ..models import IDC


__all__ = ['IDCSerializer']


class IDCSerializer(BulkSerializerMixin, ResourceSerializer):
    """
    供应商模型序列化器
    """

    class Meta:
        list_serializer_class = BulkListSerializer
        update_lookup_field = 'uuid'
        fields = '__all__'
        model = IDC
