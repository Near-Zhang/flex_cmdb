from common.viewsets import BulkManageViewSet
from ..models import Region, Zone
from ..serializers import RegionSerializer, ZoneSerializer


__all__ = ['RegionViewSet', 'ZoneViewSet']


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
