from common.viewsets import *
from ..models import CloudInterface
from ..serializers import CloudInterfaceSerializer


__all__ = ['CloudInterfaceViewSet']


class CloudInterfaceViewSet(BulkManageViewSet):
    """
    云接口视图集
    """
    queryset = CloudInterface.objects.all()
    serializer_class = CloudInterfaceSerializer
    lookup_field = 'uuid'