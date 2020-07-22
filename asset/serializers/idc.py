from common.serializers import BulkSerializerMixin, DisplaySerializer, BulkListSerializer
from ..models import IDC


__all__ = ['IDCSerializer']


class IDCSerializer(BulkSerializerMixin, DisplaySerializer):
    """
    供应商模型序列化器
    """

    class Meta:
        list_serializer_class = BulkListSerializer
        update_lookup_field = 'uuid'
        fields = '__all__'
        model = IDC
