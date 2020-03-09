from common.serializers import ResourceSerializer, BulkListSerializer
from rest_framework_bulk import BulkSerializerMixin
from ..models import CloudInterface


__all__ = ['CloudInterfaceSerializer']


class CloudInterfaceSerializer(BulkSerializerMixin, ResourceSerializer):
    """
    云接口模型序列化器
    """

    class Meta:
        list_serializer_class = BulkListSerializer
        update_lookup_field = 'uuid'
        fields = '__all__'
        model = CloudInterface