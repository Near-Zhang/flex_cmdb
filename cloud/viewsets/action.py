from common.viewsets import *
from ..models import CloudAction
from ..serializers import CloudActionSerializer


__all__ = ['CloudActionViewSet']


class CloudActionViewSet(BulkManageViewSet):
    """
    云动作视图集
    """
    queryset = CloudAction.objects.all()
    serializer_class = CloudActionSerializer
    lookup_field = 'uuid'