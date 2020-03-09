from common.serializers import ResourceSerializer, BulkListSerializer
from rest_framework_bulk import BulkSerializerMixin
from ..models import CloudAction


__all__ = ['CloudActionSerializer']


class CloudActionSerializer(BulkSerializerMixin, ResourceSerializer):
    """
    云动作模型序列化器
    """

    class Meta:
        list_serializer_class = BulkListSerializer
        update_lookup_field = 'uuid'
        fields = '__all__'
        model = CloudAction