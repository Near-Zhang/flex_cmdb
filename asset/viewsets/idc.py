from common.viewsets import *
from ..models import IDC, Region, Zone
from ..serializers import IDCSerializer, RegionSerializer, ZoneSerializer


__all__ = ['IDCViewSet', 'RegionViewSet', 'ZoneViewSet']


class IDCViewSet(BulkManageViewSet):
    """
    供应商视图集
    """
    queryset = IDC.objects.all()
    serializer_class = IDCSerializer
    lookup_field = 'uuid'


class RegionViewSet(BulkManageViewSet):
    """
    地域视图集
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    lookup_field = 'uuid'


class ZoneViewSet(BulkManageViewSet):
    """
    可用区视图集
    """
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    lookup_field = 'uuid'

