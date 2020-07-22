from common.viewsets import BulkManageViewSet
from ..models import IDC
from ..serializers import IDCSerializer


__all__ = ['IDCViewSet']


class IDCViewSet(BulkManageViewSet):
    """
    供应商视图集
    """
    queryset = IDC.objects.all()
    serializer_class = IDCSerializer
    lookup_field = 'uuid'




